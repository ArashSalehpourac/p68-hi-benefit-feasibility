#!/usr/bin/env python3
"""P68 P1 - FIFO uplink queue simulator on REAL P0 payloads -> G1 / G3 / G4 diagnostics.

Protocol: proposal_v4_final.md (frozen 2026-10-01). This script is NEW (post-freeze, 2026-10-02) and only
instantiates the frozen gate definitions; every modelling choice below is an assumption of the simulator,
NOT a result about real networks. Traces (Ghoshal 2022, Khan 2025) are NOT used (licence unresolved);
the uplink is a fitted-style log-normal AR(1) process.

What it does
  * payload pool: rows of payload_p0.csv (image, corruption, severity, codec, bytes)
  * arrivals: Poisson, load rho; single FIFO uplink; transfer rate held at its value at transmit start
  * latent log-rate: AR(1) in continuous time (tau seconds), log-normal marginal
  * delivery time = queue wait W + S/R + RTT + T_R ; deadline D ; realised Z = 1{delivery <= D}
  * oracle q_i = P(delivery <= D | decision-time state incl. queue workload W and latent rate state) via Monte Carlo
  * q-hat: logistic regression on OBSERVABLE decision-time features (noisy rate EMA, RTT EMA, W, S), cross-fitted
Outputs per (uplink median, load, sigma, D):
  G1 proxy : share of requests with oracle q in [0.05, 0.95]  (in-window share)
  coupling : mean q(clean) - mean q(noise sev>=4)   (the feasibility penalty on payload-inflating inputs)
  G3       : Var_S/(Var_S+Var_R) of transfer time T=S/R   (frozen definition; fires if < 0.10)
  G4       : within-stratum ECE of q-hat (stratum = corruption x severity, n>=150); fires if > 0.05
G1 in the protocol is defined on the BENEFIT effect (>= SESOI at >= 3 contiguous D values); P1 has no benefit G,
so the in-window share here is only a necessary-condition proxy (is q informative at all?).
"""
import argparse, json, sys
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

D_GRID_MS = [50, 100, 150, 200, 300, 400, 600, 800, 1200]


def load_pool(csv, codec, p_clean, noise_heavy):
    d = pd.read_csv(csv)
    d = d[(d.codec == codec) & (d.corruption != "ERR")].copy()
    d["bytes"] = d["bytes"].astype(float)
    d["stratum"] = d.corruption + "|" + d.severity.astype(str)
    clean = d[d.corruption == "clean"]
    cor = d[d.corruption != "clean"]
    if noise_heavy:  # stress mix: only the three additive-noise families (sev 1-5)
        cor = cor[cor.corruption.isin(["gaussian_noise", "shot_noise", "impulse_noise"])]
    return clean, cor, p_clean


def sample_requests(rng, clean, cor, p_clean, n):
    is_clean = rng.random(n) < p_clean
    out = np.empty(n, dtype=int)
    # pools as arrays of row indices into a stacked frame
    ci = rng.integers(0, len(clean), n)
    oi = rng.integers(0, len(cor), n)
    frame = pd.concat([clean, cor], ignore_index=True)
    idx = np.where(is_clean, ci, len(clean) + oi)
    return frame.iloc[idx].reset_index(drop=True)


def ece(p, z, bins=10):
    b = np.minimum((p * bins).astype(int), bins - 1)
    tot = 0.0
    for k in range(bins):
        m = b == k
        if m.any():
            tot += m.mean() * abs(p[m].mean() - z[m].mean())
    return tot


def simulate(req, mu_bps, sigma, rho, tau, rng, K=64, rtt_med=0.040, rtt_sig=0.3, srv_med=0.030, srv_sig=0.4,
             meas_sig=0.15, ema_a=0.2):
    n = len(req)
    S = req["bytes"].to_numpy()
    mu = np.log(mu_bps / 8.0)  # log of median rate in BYTES/s
    e_inv = np.exp(-mu + sigma ** 2 / 2)
    lam = rho / (S.mean() * e_inv)
    gaps = rng.exponential(1 / lam, n)
    arr = np.cumsum(gaps)
    # latent AR(1) log-rate at arrival times
    x = np.empty(n)
    x[0] = mu + sigma * rng.standard_normal()
    a_ = np.exp(-gaps / tau)
    eps = rng.standard_normal(n)
    for i in range(1, n):
        x[i] = mu + a_[i] * (x[i - 1] - mu) + sigma * np.sqrt(1 - a_[i] ** 2) * eps[i]
    W = np.empty(n); xs = np.empty(n); tx = np.empty(n)
    free = 0.0
    prop_eps = rng.standard_normal(n)
    for i in range(n):
        start = max(arr[i], free)
        W[i] = start - arr[i]
        a = np.exp(-W[i] / tau)
        xs[i] = mu + a * (x[i] - mu) + sigma * np.sqrt(1 - a ** 2) * prop_eps[i]
        tx[i] = S[i] / np.exp(xs[i])
        free = start + tx[i]
    rtt = rtt_med * np.exp(rtt_sig * rng.standard_normal(n))
    srv = srv_med * np.exp(srv_sig * rng.standard_normal(n))
    T = W + tx + rtt + srv  # realised delivery time
    # observable features: noisy EMA of PAST measured throughput, EMA of past RTT
    meas_rate = np.exp(xs + meas_sig * rng.standard_normal(n))  # measured rate of each transfer
    ema_rate = np.empty(n); ema_rtt = np.empty(n)
    er, et = np.exp(mu), rtt_med
    for i in range(n):  # features at decision time use only transfers that FINISHED before? approximate: previous requests
        ema_rate[i] = er; ema_rtt[i] = et
        er = (1 - ema_a) * er + ema_a * meas_rate[i]
        et = (1 - ema_a) * et + ema_a * rtt[i] * np.exp(meas_sig * rng.standard_normal())
    # oracle components: MC over rate at start, RTT, server time given decision-time latent state
    a = np.exp(-W / tau)[:, None]
    mean_c = mu + a * (x[:, None] - mu)
    sd_c = sigma * np.sqrt(1 - a ** 2)
    xk = mean_c + sd_c * rng.standard_normal((n, K))
    txk = S[:, None] / np.exp(xk)
    rk = rtt_med * np.exp(rtt_sig * rng.standard_normal((n, K)))
    sk = srv_med * np.exp(srv_sig * rng.standard_normal((n, K)))
    base = W[:, None] + txk + rk + sk  # K draws of delivery time
    # G3 moments on transfer time (rate at start), unconditional on queue
    U = 1.0 / np.exp(xs)
    var_S = S.var() * U.mean() ** 2
    var_R = S.mean() ** 2 * U.var()
    g3 = var_S / (var_S + var_R)
    feats = np.c_[W, S / ema_rate, ema_rtt, S]
    return dict(base=base, T=T, W=W, feats=feats, g3=g3, lam=lam, rho_emp=float((S * 1.0 / np.exp(xs)).sum() / arr[-1]))


def evaluate(req, sim, D, rng):
    q = (sim["base"] <= D).mean(axis=1)  # oracle q
    Z = (sim["T"] <= D).astype(float)
    n = len(Z); h = n // 2
    Wf, txh, rtth, Sf = sim["feats"].T
    tot = Wf + txh + rtth + 0.030  # known mean server-time offset
    F = np.c_[np.log(tot / D), np.log(tot / D) ** 2, np.log(Wf + 1e-3), np.log(txh), np.log(rtth), np.log(Sf)]
    X = StandardScaler().fit(F[:h]).transform(F)
    X2 = StandardScaler().fit(F[h:]).transform(F)
    qh = np.empty(n)
    for tr, te, XX in ((slice(0, h), slice(h, n), X), (slice(h, n), slice(0, h), X2)):  # 2-fold cross-fit
        z = Z[tr]
        if z.min() == z.max():
            qh[te] = z.mean(); continue
        m = LogisticRegression(C=10.0, max_iter=500).fit(XX[tr], z)
        qh[te] = m.predict_proba(XX[te])[:, 1]
    st = req["stratum"].to_numpy()
    ece_s, w_s = [], []
    for s in np.unique(st):
        m = st == s
        if m.sum() >= 150:
            ece_s.append(ece(qh[m], Z[m])); w_s.append(m.sum())
    ece_w = float(np.average(ece_s, weights=w_s)) if ece_s else np.nan
    ece_max = float(np.max(ece_s)) if ece_s else np.nan
    sev = req.severity.to_numpy(); cor = req.corruption.to_numpy()
    noisy = np.isin(cor, ["gaussian_noise", "shot_noise", "impulse_noise"]) & (sev >= 4)
    clean = cor == "clean"
    return dict(D_ms=int(D * 1000), inwin=float(((q >= .05) & (q <= .95)).mean()), q_mean=float(q.mean()),
                q_clean=float(q[clean].mean()) if clean.any() else np.nan,
                q_noise45=float(q[noisy].mean()) if noisy.any() else np.nan,
                coupling=float(q[clean].mean() - q[noisy].mean()) if clean.any() and noisy.any() else np.nan,
                Z_mean=float(Z.mean()), ece_oracle=float(ece(q, Z)), ece_qhat_overall=float(ece(qh, Z)),
                ece_qhat_stratum_w=ece_w, ece_qhat_stratum_max=ece_max,
                auc_gap=float(np.corrcoef(q, qh)[0, 1]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", default="p1_results.csv")
    ap.add_argument("--codec", default="jpeg")
    ap.add_argument("--n", type=int, default=40000)
    ap.add_argument("--p_clean", type=float, default=0.5)
    ap.add_argument("--noise_heavy", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--rates", default="1,2,5,10,20", help="median uplink rate, Mbit/s")
    ap.add_argument("--loads", default="0.3,0.6,0.85")
    ap.add_argument("--sigmas", default="0.6")
    ap.add_argument("--tau", type=float, default=2.0)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    clean, cor, pc = load_pool(a.csv, a.codec, a.p_clean, a.noise_heavy)
    rows = []
    for R in map(float, a.rates.split(",")):
        for sg in map(float, a.sigmas.split(",")):
            for rho in map(float, a.loads.split(",")):
                req = sample_requests(rng, clean, cor, pc, a.n)
                sim = simulate(req, R * 1e6, sg, rho, a.tau, rng)
                for D in D_GRID_MS:
                    r = evaluate(req, sim, D / 1000.0, rng)
                    r.update(rate_mbps=R, sigma=sg, rho=rho, g3=sim["g3"], codec=a.codec, noise_heavy=a.noise_heavy,
                             n=a.n, W_median_ms=float(np.median(sim["W"]) * 1000))
                    rows.append(r)
                print(f"done R={R} sigma={sg} rho={rho} g3={sim['g3']:.3f}", file=sys.stderr)
    out = pd.DataFrame(rows)
    out.to_csv(a.out, index=False)
    json.dump(vars(a), open(a.out.replace(".csv", "_args.json"), "w"), indent=1)
    print(f"wrote {a.out} ({len(out)} rows)")


if __name__ == "__main__":
    main()
