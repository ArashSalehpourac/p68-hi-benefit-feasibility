# P2 direct Cov(G,q) check (post-freeze, 2026-10-02)

Script: scripts/p2_direct_q.py. 100,000 requests sampled from the 260,000 P2 inputs (50% clean),
P1 simulator (assumed network), 10 rate x load configs, D = c*T0, c in {1.00,1.15,1.30,1.50,1.75},
within-stratum corr(G,q), strata corruption x severity x class, image-cluster bootstrap (100 draws).

| Pair | Family | sign match | mean corr | CI excludes 0 |
|---|---|---|---|---|
| A | additive | 0.38 | +0.0008 | 0.00 |
| A | reductive | 0.36 | -0.0034 | 0.10 |
| B | additive | 0.34 | +0.0016 | 0.06 |
| B | reductive | 0.44 | -0.0023 | 0.04 |

Predicted: Cov(G,q)<0 additive, >0 reductive. Result: |mean corr| <= 0.0034, no support; agrees with the
bytes-proxy result, G2 stands. Caveats: assumed simulator network, 100 bootstrap draws, sampled requests.
