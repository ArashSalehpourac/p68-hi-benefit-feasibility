"""P68 post-freeze check: direct within-stratum Cov(G, q) on the P2 inputs, q from the P1 queue simulator (assumed network).
Colab usage (no GPU needed):
  OUT = "/content/drive/MyDrive/P68/outputs/p2"; SIM = <folder containing p1_queue_sim_v2.py>
  exec(open(SIM + "/p2_direct_q.py").read())
Pre-registered direction: additive (noise) kappa_mech = Cov(G,q) < 0 ; reductive (blur, contrast) > 0.
"""
import os, sys, numpy as np, pandas as pd
OUT = globals().get("OUT", "/content/drive/MyDrive/P68/outputs/p2")
SIM = globals().get("SIM", OUT)
N = globals().get("N_REQ", 100000); BOOT = globals().get("BOOT", 100)
sys.path.insert(0, SIM); import p1_queue_sim_v2 as P
PAIRS = {"A": ("mobilenet_v3_small", "convnext_base"), "B": ("resnet18", "vit_b_16")}
ADD = ["gaussian_noise", "shot_noise", "impulse_noise"]; RED = ["defocus_blur", "contrast"]
D0 = pd.read_csv(f"{OUT}/p2_inputs.csv")
for p, (L, R) in PAIRS.items():
    D0[f"G_{p}"] = (D0[f"{R}_pred"] == D0.label).astype(int) - (D0[f"{L}_pred"] == D0.label).astype(int)
D0["bytes"] = D0["bytes"].astype(float); D0["stratum"] = D0.corruption + "|" + D0.severity.astype(str)
clean, cor = D0[D0.corruption == "clean"], D0[D0.corruption != "clean"]

def within_stat(df, x, g, w):
    key = df.groupby(["corruption", "severity", "label"], sort=False).ngroup().to_numpy()
    G, X = df[g].to_numpy(float), np.asarray(x, float); K = key.max() + 1
    n = np.bincount(key, w, K); mg = np.bincount(key, w * G, K) / np.maximum(n, 1e-9); mx = np.bincount(key, w * X, K) / np.maximum(n, 1e-9)
    dg, dx = G - mg[key], X - mx[key]
    c = np.bincount(key, w * dg * dx, K); vg = np.bincount(key, w * dg * dg, K); vx = np.bincount(key, w * dx * dx, K)
    ok = n > 2; den = (n[ok] - 1).sum()
    cov, VG, VX = c[ok].sum() / den, vg[ok].sum() / den, vx[ok].sum() / den
    return cov / np.sqrt(VG * VX + 1e-18)

rng = np.random.default_rng(0); rows = []
for R_, rho in [(r, l) for r in (1, 2, 5, 10, 20) for l in (0.3, 0.6)]:
    ci = rng.integers(0, len(clean), N); oi = rng.integers(0, len(cor), N); isc = rng.random(N) < 0.5
    req = pd.concat([clean, cor], ignore_index=True).iloc[np.where(isc, ci, len(clean) + oi)].reset_index(drop=True)
    sim = P.simulate(req, R_ * 1e6, 0.6, rho, 2.0, rng)
    T0 = float(np.median(sim["T"][(req.corruption == "clean").to_numpy()]))
    u, inv = np.unique(req.image_idx.to_numpy(), return_inverse=True)
    for c in (1.00, 1.15, 1.30, 1.50, 1.75):
        q = (sim["base"] <= c * T0).mean(axis=1); req["q"] = q
        for pair in PAIRS:
            for fam, cs, pred in (("additive", ADD, "<0"), ("reductive", RED, ">0")):
                m = req.corruption.isin(cs).to_numpy(); sub = req[m]
                if sub.q.std() < 1e-6: continue
                est = within_stat(sub, sub.q, f"G_{pair}", np.ones(len(sub)))
                bs = []
                for _ in range(BOOT):
                    cnt = rng.multinomial(len(u), np.full(len(u), 1 / len(u)))
                    bs.append(within_stat(sub, sub.q, f"G_{pair}", cnt[inv[m]].astype(float)))
                lo, hi = np.percentile(bs, [2.5, 97.5])
                rows.append(dict(rate_mbps=R_, load=rho, c=c, T0_ms=T0 * 1e3, pair=pair, family=fam, pred_sign=pred, corr_G_q=est, ci_lo=lo, ci_hi=hi,
                                 sign_matches=(est < 0) if fam == "additive" else (est > 0), ci_excl_0=bool(lo > 0 or hi < 0)))
    print("done", R_, rho, flush=True)
    pd.DataFrame(rows).to_csv(f"{OUT}/summary_p2_direct_Gq.csv", index=False)
R = pd.DataFrame(rows)
print(R.groupby(["pair", "family"]).agg(cells=("corr_G_q", "size"), sign_match=("sign_matches", "mean"), mean_corr=("corr_G_q", "mean"), excl0=("ci_excl_0", "mean")).round(4))
