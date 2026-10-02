#!/usr/bin/env python3
"""P68 post-freeze (2026-10-02) checks: C1 window vs T0 and G4(b) per-stratum bias-sign. Simulator = p1_queue_sim_v2 (assumed network)."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1_queue_sim_v2 as P
import p1_calib_diag as C
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
N = int(sys.argv[1]) if len(sys.argv) > 1 else 40000
CS = [1.00, 1.15, 1.30, 1.50, 1.75]
rng = np.random.default_rng(7); C._rng = np.random.default_rng(11)
clean, cor, pc = P.load_pool("payload_p0.csv", "jpeg", 0.5, False)
rows = []
for R in [1, 2, 5, 10, 20]:
    for rho in [0.3, 0.6, 0.85]:
        req = P.sample_requests(rng, clean, cor, pc, N); sim = P.simulate(req, R * 1e6, 0.6, rho, 2.0, rng)
        isc = (req.corruption == "clean").to_numpy(); T0 = float(np.median(sim["T"][isc]))
        st = req["stratum"].to_numpy(); Wf, txh, rtth, Sf = sim["feats"].T; n = len(Wf); h = n // 2
        sev = req.severity.to_numpy(); cn = req.corruption.to_numpy()
        noisy = np.isin(cn, ["gaussian_noise", "shot_noise", "impulse_noise"]) & (sev >= 4)
        for c in CS:
            D = c * T0; Z = (sim["T"] <= D).astype(float); q = (sim["base"] <= D).mean(axis=1)
            inwin = float(((q >= .05) & (q <= .95)).mean()); coup = float(q[isc].mean() - q[noisy].mean())
            tot = Wf + txh + rtth + 0.030
            F = np.c_[np.log(tot / D), np.log(tot / D) ** 2, np.log(Wf + 1e-3), np.log(txh), np.log(rtth), np.log(Sf)]
            qh = np.empty(n)
            qh[h:] = C.fit_predict(F, Z, slice(0, h), slice(h, n), "logit"); qh[:h] = C.fit_predict(F, Z, slice(h, n), slice(0, h), "logit")
            e = C.strat_ece(qh, Z, st, B=60)
            ex = e[e.exceeds_null95]; bias = (e.mean_qhat - e.mean_Z)
            exb = (ex.mean_qhat - ex.mean_Z)
            share = len(ex) / max(len(e), 1)
            same = max((exb > 0).mean(), (exb < 0).mean()) if len(ex) else np.nan
            a_excess = float(np.average(e.ece, weights=e.n) - np.average(e.ece_null_mean, weights=e.n))
            rows.append(dict(rate=R, load=rho, c=c, T0_ms=T0 * 1e3, D_ms=D * 1e3, inwin=inwin, coupling=coup, q_clean=float(q[isc].mean()),
                             n_strata=len(e), ece_excess_over_null=a_excess, G4a_fires=a_excess > 0.02, share_exceed_null95=share,
                             n_exceed=len(ex), exceed_same_sign_frac=same, mean_bias_exceeding=float(exb.mean()) if len(ex) else np.nan,
                             G4b_fires=bool(share > 0.15 and len(ex) and same >= 0.75)))
        print("done", R, rho, f"T0={T0*1e3:.0f}ms", flush=True)
        pd.DataFrame(rows).to_csv("p1_c1_g4b.csv", index=False)
