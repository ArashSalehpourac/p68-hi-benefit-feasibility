# P68 — P2 robustness check and decision (2026-10-02)

Post-freeze, descriptive. proposal_v4_final.md (SHA-256 3d40c2d3…f89b73) is unchanged.

Local model rescored on JPEG-decoded pixels (20 images/class, 4000 images). Within-stratum corr of G with bytes (image-cluster bootstrap 95% CI):

| Pair | Family | Raw local | JPEG local |
|---|---|---|---|
| A | additive | -0.0019 [-0.0143, 0.0101] | 0.0031 [-0.0096, 0.0135] |
| A | reductive | 0.0267 [0.0110, 0.0401] | 0.0172 [0.0015, 0.0317] |
| B | additive | 0.0097 [-0.0043, 0.0225] | 0.0092 [-0.0043, 0.0230] |
| B | reductive | 0.0265 [0.0122, 0.0403] | 0.0200 [0.0064, 0.0337] |

Full 10,000-image run, pooled / between-cell / within-stratum correlation:

| Pair | Family | Pooled | Between-cell | Within |
|---|---|---|---|---|
| A | additive | 0.026 | 0.212 | -0.012 |
| A | reductive | 0.040 | 0.374 | 0.017 |
| B | additive | 0.076 | 0.556 | 0.009 |
| B | reductive | 0.026 | 0.056 | 0.026 |

Raw-vs-JPEG asymmetry is not the cause. Additive: pair A reversed on the full run (CI excludes 0), pair B null. Reductive: reversed in both pairs. G2 fires. Coupling exists between corruption x severity cells, not within strata.

Decision: close P68 as a negative/boundary result; short negative-result note; full study blocked.
Script: scripts/p2_robust_cell.py (needs main P2 notebook state). Data in Drive P68/outputs/p2.
