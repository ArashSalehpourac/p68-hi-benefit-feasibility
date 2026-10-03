# P68-R1K — Causal feasibility q-hat freeze

Date: 2026-10-03  
Status: **FROZEN — raw causal logistic selected by the pre-specified network-only rule**

## Inputs and leakage status

R1K used only:
- the frozen 6,184-row PAM'25 joint UL+RTT trace;
- the frozen P0 payload distributions;
- the frozen 60–110 ms network-component deadline grid.

No inference benefit, correctness, confidence, top-1 outcome, or policy endpoint was loaded.

## Cross-validation

Five deterministic temporal-block folds, balanced within operator × drive.

For outer fold k:
- fold k = test;
- fold (k+1) mod 5 = calibration;
- remaining three folds = training.

Every frozen block is test once and calibration once.

## Candidates

1. raw causal logistic;
2. global isotonic calibration;
3. operator×drive-aware regularized Platt calibration.

Eligibility was frozen before execution:
- Brier skill > 0.20 in every codec × deadline cell;
- ROC AUC >= 0.75 in every cell.

Selection among eligible candidates:
1. minimum maximum operator×drive ECE10 across all 12 cells;
2. minimum median worst-stratum ECE10;
3. minimum maximum pooled ECE10;
4. maximum median Brier skill.

## Result

Eligible:
- raw logistic: YES;
- global isotonic: YES;
- group-aware Platt: NO (minimum Brier skill 0.177943).

Selected by the frozen rule: **raw_logistic**.

Raw logistic across the 12 codec × deadline cells:
- minimum Brier skill: 0.220830;
- median Brier skill: 0.272020;
- minimum AUC: 0.804990;
- median AUC: 0.813456;
- maximum pooled ECE10: 0.060741;
- maximum worst operator×drive ECE10: 0.099692;
- median worst operator×drive ECE10: 0.087118.

Global isotonic had much better pooled ECE (maximum 0.031069) but worse conditional calibration under the frozen primary criterion (maximum worst-stratum ECE10 0.107563) and slightly lower discrimination / Brier skill.

Group-aware Platt did not solve the conditional-calibration problem and failed the frozen Brier-skill eligibility rule.

## Freeze decision

For subsequent measured-trace replay and the factorized policy, q-hat is the **raw causal logistic probability** using the R1J frozen past-only feature set and block-level fitting protocol.

This is a deliberately conservative freeze to prevent further nuisance-model tuning after inference benefit outcomes are exposed.

The residual conditional calibration error (~0.10 worst-stratum ECE) must be reported as a limitation and audited in operator×drive sensitivity tables. It is not evidence that q-hat is a perfectly calibrated probability.

Next pre-R2/R3 item: hardware-specific remote-compute latency for ConvNeXt-Base and ViT-B/16 under batch-1 online inference semantics.
