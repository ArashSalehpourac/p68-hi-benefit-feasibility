"""
Synthetic check: does deadline-censored feedback bias online HI routing?
(Result: no censoring bias when stationary; coupling effect only in an intermediate window.
Crude screen, arbitrary parameters, one channel shift - NOT a proof.)

Bins c=0..9 (0 = lowest local confidence). Latent hardness h in bin ~ U(lo,hi).
Local wrong w.p. h; remote wrong w.p. 0.1.  G = remote_correct - local_correct.
Payload S = exp(kappa*(h-0.5)); completion Z ~ Bern(sigmoid(beta*(s0 - log S) + ch)).
kappa>0: hard => big => late (the hypothesised coupling). kappa=0: no coupling.
Learners see remote labels ONLY on completed offloads (local correctness inferred
from the remote output as pseudo-label, as in HI).
  blind : offload iff mean(G | completed, bin) > lam      (ignores completion)
  adj   : offload iff mean(G | completed, bin) * qhat(bin) > lam   (E[ZG|c] estimator)
Utility = E[A*(Z*G - lam)] in deployment. Oracle knows true E[ZG|bin] in deployment.
"""
import numpy as np, sys
rng = np.random.default_rng(0)
NB = 10; LAM = 0.12; BETA = 3.0; S0 = 0.0

def draw(n, kappa, ch):
    b = rng.integers(0, NB, n)
    lo = 0.9 - 0.09 * (b + 1); hi = 0.9 - 0.09 * b          # bin0 hardest
    h = rng.uniform(np.clip(lo, 0.0, 1), np.clip(hi, 0.0, 1) + 1e-9)
    lw = rng.random(n) < h; rw = rng.random(n) < 0.1
    G = (~rw).astype(int) - (~lw).astype(int)
    logS = kappa * (h - 0.5)
    p = 1 / (1 + np.exp(-(BETA * (S0 - logS) + ch)))
    Z = rng.random(n) < p
    return b, G, Z

def learn(n, kappa, ch, eps=0.3):
    sG = np.zeros(NB); nC = np.zeros(NB); nA = np.zeros(NB)
    b, G, Z = draw(n, kappa, ch)
    for i in range(n):
        k = b[i]
        if rng.random() < eps or nC[k] < 5:       # exploration / warm start: attempt offload
            nA[k] += 1
            if Z[i]:
                nC[k] += 1; sG[k] += G[i]
    ghat = np.where(nC > 0, sG / np.maximum(nC, 1), 0)
    qhat = np.where(nA > 0, nC / np.maximum(nA, 1), 0)
    return ghat, qhat

def deploy(policy, kappa, ch, n=200000):
    b, G, Z = draw(n, kappa, ch)
    A = policy[b]
    u = A * (Z * G - LAM)
    hard = b < 3
    return u.mean(), u[hard].mean()

def oracle(kappa, ch, n=200000):
    b, G, Z = draw(n, kappa, ch)
    pol = np.array([(Z * G)[b == k].mean() > LAM for k in range(NB)])
    return pol

def run(kappa, ch_train, ch_dep, reps=20, n=40000):
    out = {"oracle": [], "blind": [], "adj": []}; hard = {k: [] for k in out}
    for _ in range(reps):
        g, q = learn(n, kappa, ch_train)
        pols = {"blind": g > LAM, "adj": g * q > LAM, "oracle": oracle(kappa, ch_dep)}
        for k, p in pols.items():
            m, mh = deploy(p, kappa, ch_dep); out[k].append(m); hard[k].append(mh)
    return {k: (np.mean(v), np.mean(hard[k])) for k, v in out.items()}

print(f"{'kappa':>5} {'train->dep':>11} | {'oracle':>7} {'adj':>7} {'blind':>7} | regret adj  blind | hard-bin regret adj blind")
for kappa in [0, 2, 4, 6]:
    for (tr, dp) in [(0.5, 0.5), (0.5, -1.0)]:
        r = run(kappa, tr, dp)
        o, oh = r["oracle"]
        print(f"{kappa:5d} {tr:+.1f}->{dp:+.1f}   | {o:7.4f} {r['adj'][0]:7.4f} {r['blind'][0]:7.4f} |"
              f"       {o-r['adj'][0]:6.4f} {o-r['blind'][0]:6.4f} |        {oh-r['adj'][1]:6.4f} {oh-r['blind'][1]:6.4f}")

# Diagnostic: naive benefit estimate from completed offloads vs true mean G, hardest bin
print("\nHardest-bin benefit: true E[G] vs completed-only estimate vs true E[ZG]")
for kappa in [0, 2, 4, 6]:
    b, G, Z = draw(400000, kappa, 0.5)
    m = b == 0
    print(f"kappa={kappa}: E[G]={G[m].mean():.3f}  E[G|Z=1]={G[m & Z].mean():.3f}  P(Z=1)={Z[m].mean():.3f}  E[ZG]={(Z*G)[m].mean():.3f}")
