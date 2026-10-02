#!/usr/bin/env python3
"""P68 P1 calibration diagnostic: per-stratum ECE of q-hat, with isotonic recalibration and a GBM alternative.
Imports simulate()/ece() from p1_queue_sim_v2.py (same directory). Feasibility-only; assumed network.
Usage: python p1_calib_diag.py --csv payload_p0.csv --out_prefix p1_calib --n 200000
"""
import argparse, sys, os
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1_queue_sim_v2 as P
from sklearn.linear_model import LogisticRegression
from sklearn.isotonic import IsotonicRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler

CONFIGS = {  # (rate Mbit/s, load): deadlines (ms) around the window
    (1.0, 0.30): [160, 200, 240], (1.0, 0.60): [160, 200, 240], (2.0, 0.30): [120, 140, 180],
    (10.0, 0.30): [80, 100, 120], (5.0, 0.60): [100, 120]}

_rng = np.random.default_rng(123)

def strat_ece(p, z, st, minn=150, B=100):
    """Per-stratum ECE plus a parametric-bootstrap null: ECE of Z* ~ Bernoulli(p) (perfect calibration, same p and n).
    ece_null95 = 95th percentile of the null; exceeds = observed ECE above it."""
    out = []
    for s in np.unique(st):
        m = st == s
        if m.sum() >= minn:
            pm = p[m]; nul = [P.ece(pm, (_rng.random(len(pm)) < pm).astype(float)) for _ in range(B)]
            e = P.ece(pm, z[m])
            out.append((s, int(m.sum()), e, float(np.mean(nul)), float(np.percentile(nul, 95)), bool(e > np.percentile(nul, 95)),
                        float(pm.mean()), float(z[m].mean())))
    return pd.DataFrame(out, columns=["stratum", "n", "ece", "ece_null_mean", "ece_null95", "exceeds_null95", "mean_qhat", "mean_Z"])

def fit_predict(F, Z, tr, te, kind):
    sc = StandardScaler().fit(F[tr]); X = sc.transform(F)
    if kind == "logit":
        m = LogisticRegression(C=10.0, max_iter=500).fit(X[tr], Z[tr]); return m.predict_proba(X[te])[:, 1]
    if kind == "logit_iso":
        idx = np.arange(len(Z))[tr]; k = int(0.8 * len(idx)); a, b = idx[:k], idx[k:]
        m = LogisticRegression(C=10.0, max_iter=500).fit(X[a], Z[a])
        iso = IsotonicRegression(out_of_bounds="clip", y_min=0, y_max=1).fit(m.predict_proba(X[b])[:, 1], Z[b])
        return iso.predict(m.predict_proba(X[te])[:, 1])
    if kind == "gbm":
        m = HistGradientBoostingClassifier(max_iter=150, learning_rate=0.1, random_state=0).fit(X[tr], Z[tr])
        return m.predict_proba(X[te])[:, 1]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--csv", required=True); ap.add_argument("--out_prefix", default="p1_calib")
    ap.add_argument("--n", type=int, default=200000); ap.add_argument("--seed", type=int, default=0); ap.add_argument("--codec", default="jpeg")
    a = ap.parse_args(); rng = np.random.default_rng(a.seed)
    clean, cor, pc = P.load_pool(a.csv, a.codec, 0.5, False)
    summ, worst = [], []
    for (R, rho), dl in CONFIGS.items():
        req = P.sample_requests(rng, clean, cor, pc, a.n); sim = P.simulate(req, R * 1e6, 0.6, rho, 2.0, rng)
        st = req["stratum"].to_numpy(); Wf, txh, rtth, Sf = sim["feats"].T; n = len(Wf); h = n // 2
        for D in dl:
            Dd = D / 1000.0; Z = (sim["T"] <= Dd).astype(float); q = (sim["base"] <= Dd).mean(axis=1)
            tot = Wf + txh + rtth + 0.030
            F = np.c_[np.log(tot / Dd), np.log(tot / Dd) ** 2, np.log(Wf + 1e-3), np.log(txh), np.log(rtth), np.log(Sf)]
            r = dict(rate=R, load=rho, D_ms=D)
            e_or = strat_ece(q, Z, st); r["oracle_w"] = np.average(e_or.ece, weights=e_or.n); r["oracle_max"] = e_or.ece.max()
            for kind in ["logit", "logit_iso", "gbm"]:
                qh = np.empty(n)
                qh[h:] = fit_predict(F, Z, slice(0, h), slice(h, n), kind); qh[:h] = fit_predict(F, Z, slice(h, n), slice(0, h), kind)
                e = strat_ece(qh, Z, st)
                r[f"{kind}_w"] = float(np.average(e.ece, weights=e.n)); r[f"{kind}_max"] = float(e.ece.max()); r[f"{kind}_n_gt05"] = int((e.ece > 0.05).sum())
                r[f"{kind}_null_mean_w"] = float(np.average(e.ece_null_mean, weights=e.n)); r[f"{kind}_n_exceed_null95"] = int(e.exceeds_null95.sum()); r[f"{kind}_n_strata"] = len(e)
                r[f"{kind}_signed_bias_w"] = float(np.average(e.mean_qhat - e.mean_Z, weights=e.n))
                if kind == "logit":
                    w = e.sort_values("ece", ascending=False).head(5).assign(rate=R, load=rho, D_ms=D); worst.append(w)
            summ.append(r); print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()}, flush=True)
    pd.DataFrame(summ).to_csv(f"{a.out_prefix}_summary.csv", index=False)
    pd.concat(worst).to_csv(f"{a.out_prefix}_worst_strata.csv", index=False)
    print(pd.concat(worst).round(3).to_string(index=False))

if __name__ == "__main__":
    main()
