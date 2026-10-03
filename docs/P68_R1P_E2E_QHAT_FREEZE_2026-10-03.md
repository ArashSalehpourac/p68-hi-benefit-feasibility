# P68-R1P — End-to-end causal q-hat freeze

Date: 2026-10-03
Status: **FROZEN — ALL 44 CELLS PASS**

R1P was the final outcome-blind nuisance-model audit before inference benefit G is exposed.

## Frozen design

- E2E support window: 70–120 ms;
- primary deadline: 95 ms;
- q-hat architecture: R1K raw logistic, no post-hoc calibration;
- features: payload bytes, previous throughput/RTT, observation age, 1-s-half-life past EMA throughput/RTT, history count, cold start, operator, drive;
- current-row throughput and RTT forbidden as q-hat inputs;
- exact R1K five block folds reused;
- realized E2E target includes measured PAM network latency plus a deterministic draw from the payload-size-decile-matched empirical R1N service distribution;
- probability calibration reference q-star is the exact empirical payload-size-decile service CDF.

## Frozen gate

Every pair × codec × deadline cell had to satisfy:
- Brier skill vs fold-specific train marginal > 0.20;
- ROC AUC >= 0.75;
- pooled q-star ECE10 <= 0.10;
- worst operator×drive q-star ECE10 <= 0.15.

All **44/44 cells pass**.

Across all cells:
- minimum Brier skill: 0.224711;
- minimum AUC: 0.803440;
- maximum pooled q-star ECE10: 0.063882;
- maximum worst-stratum q-star ECE10: 0.108894.

At the primary 95-ms deadline, the weakest cell still satisfies:
- minimum Brier skill: 0.272730;
- minimum AUC: 0.811799;
- maximum pooled q-star ECE10: 0.063882;
- maximum worst-stratum q-star ECE10: 0.108894.

Primary 95-ms cells:
- A/JPEG: Brier skill 0.291439, AUC 0.817472, q-star ECE10 0.058906, worst-stratum 0.090431;
- A/WebP: 0.305681, 0.821362, 0.054828, 0.085021;
- B/JPEG: 0.272730, 0.811799, 0.063882, 0.108894;
- B/WebP: 0.288828, 0.817066, 0.060323, 0.101785.

## Decision

The E2E feasibility estimator is frozen as the raw causal logistic specification above. No further q-hat tuning is permitted after benefit G is exposed.

The nuisance-design phase is closed. R2 may now load the frozen historical P2 JPEG benefit evidence. R3 policy benchmarking remains blocked until its SESOI/equivalence rule is explicitly frozen.