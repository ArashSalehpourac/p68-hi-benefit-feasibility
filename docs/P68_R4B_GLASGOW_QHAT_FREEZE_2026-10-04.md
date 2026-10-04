# P68-R4B — Glasgow causal q-hat replication audit (FROZEN BEFORE EXECUTION)

Date: 2026-10-04  
Status: **FROZEN BEFORE R4B EXECUTION**

R4B is outcome-blind. It must not load P2 inference benefit, correctness, confidence, factorized-policy outcomes or joint-policy outcomes.

## Purpose

Before policy replication on Glasgow, verify that a deployable causal feasibility estimator can predict E2E success at the independently frozen Glasgow support window.

## Primary network family

Glasgow 5G Dataset 2025 canonical trace from R4A:
- 720 sessions;
- 24 blocks = date × provider × device;
- 30 sessions/block.

## Frozen deadline support

Audit exactly:
- 30 ms;
- 35 ms;
- 40 ms.

Primary deadline: **35 ms**.

## Causal feature semantics

Use the R1J/R1P architecture adapted only for Glasgow context names.

Numeric:
- payload_bytes;
- prev_upload_mbps;
- prev_ping_ms;
- network_age_ms;
- ema1s_upload_mbps;
- ema1s_ping_ms;
- history_count;
- cold_start.

Categorical:
- provider;
- device.

Forbidden:
- current upload throughput;
- current ping;
- realized service latency;
- realized E2E success as an input;
- inference benefit/correctness/confidence/policy outcome.

Location is not used as a q-hat feature.

## Temporal feature construction

Within each frozen date×provider×device block:
- sort by timestamp;
- prior-state features use only earlier rows in the block;
- EMA half-life = 1000 ms;
- first row is cold start.

## Cross-validation

Use **leave-one-date-out** evaluation:
- 3 outer folds;
- each date is test once;
- other 2 dates are training.

No request-level IID split.

This is intentionally stronger than random block folding and directly tests day-to-day generalization.

## Target

For each pair and request:

`Y_e2e = 1{ping + serialization + sampled_remote_service <= D}`.

Service realization is deterministic from the frozen empirical R1N JPEG payload-size-decile distribution.

Calibration reference:

`q_star = F_service,decile(D - ping - serialization)`.

## Frozen model

Raw logistic regression exactly following R1P:
- numeric median imputation;
- missing indicators;
- standardization;
- provider/device one-hot encoding;
- L2 logistic regression;
- C = 1.0;
- no post-hoc calibration.

No alternative model or hyperparameter search.

## Gate

Every pair × deadline cell (2 × 3 = 6 cells) must satisfy:
- Brier skill vs train-fold marginal > 0.20;
- ROC AUC >= 0.75;
- pooled q-star ECE10 <= 0.10;
- worst provider×device q-star ECE10 <= 0.15.

All 6 cells must pass for q-hat to be frozen for R4C policy replication.

If any cell fails, no model reselection is permitted after policy outcomes; redesign must occur while still outcome-blind.
