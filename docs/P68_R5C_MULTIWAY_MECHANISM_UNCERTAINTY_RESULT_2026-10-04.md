# P68-R5C — Multiway mechanism-uncertainty result

Date: 2026-10-04  
Status: **PASS — POINT ESTIMATES REPRODUCED; NETWORK/SERVICE UNCERTAINTY DOES NOT CHANGE THE MAGNITUDE CONCLUSION**

R5C executed without errors from the pre-execution freeze at:

`bfae6d679fdc8714d543134fbfc6ee974e05aab8`

The exact frozen P2, PAM, Glasgow, and remote-service hashes matched. All eight primary mechanism point estimates reproduced the previously frozen R2/R4C gaps to <5e-6 pp.

## Three-way primary uncertainty

The primary R5C interval resamples:
- ImageNet class;
- measured network temporal block;
- sustained-warm remote-service measurement round.

### PAM, 95 ms

- A/additive: gap **+0.006495 pp**, 95% CI **[+0.001125,+0.012223] pp**
- A/reductive: **-0.012572 pp**, CI **[-0.022019,-0.004003] pp**
- B/additive: **-0.004333 pp**, CI **[-0.010264,+0.001700] pp**
- B/reductive: **-0.017780 pp**, CI **[-0.026776,-0.009289] pp**

### Glasgow, 35 ms

- A/additive: gap **+0.001956 pp**, 95% CI **[-0.000322,+0.004810] pp**
- A/reductive: **-0.000540 pp**, CI **[-0.004137,+0.003542] pp**
- B/additive: **-0.001190 pp**, CI **[-0.003179,+0.000795] pp**
- B/reductive: **-0.003052 pp**, CI **[-0.006003,-0.000361] pp**

## Effect of adding network and service uncertainty

For PAM, adding network-block and service-round uncertainty changes the intervals only modestly.

For Glasgow, service-round resampling widens intervals more noticeably because the network family has only 24 temporal blocks and the service benchmark has five rounds. In particular, A/additive no longer excludes zero under the full three-way bootstrap.

This does not alter the scientific magnitude conclusion: all factorization gaps remain on the order of thousandths to hundredths of a percentage point.

## Interpretation

The mechanism claim should be framed by **effect size**, not statistical significance.

The defensible statement is that under exogenous measured-network replay, the payload-mediated within-stratum interaction term is extremely small across PAM and Glasgow, even after propagating uncertainty from workload classes, measured network blocks, and empirical remote-service rounds.

Do not claim that every gap is statistically nonzero or that the result proves general conditional independence.
