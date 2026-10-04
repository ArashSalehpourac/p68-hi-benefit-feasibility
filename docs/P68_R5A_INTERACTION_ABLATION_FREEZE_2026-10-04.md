# P68-R5A — Matched-capacity interaction ablation and detectability positive control

Date: 2026-10-04  
Status: **FROZEN BEFORE R5A EXECUTION**

## Motivation

The external peer review identified a remaining identification problem in R3B: the factorized policy and the joint policy differ not only in cross-side interaction flexibility but also in estimation target and model form. Therefore the observed joint-minus-factorized gain cannot be attributed uniquely to interaction learning.

R5A addresses this by comparing two **direct-utility HGBR models** that use:
- the same target;
- the same rows;
- the same folds;
- the same feature set;
- the same HGBR hyperparameters;
- the same training procedure;
- the same held-out budgets.

They differ only in whether image-side and network-side features are allowed to interact.

## Data and replay

Reuse the exact valid R3B construction:
- frozen P2 JPEG-q75 workload;
- frozen PAM measured UL+RTT trace;
- frozen R1N empirical service distribution;
- frozen R3B image-fold assignment;
- frozen R3B trace-block assignment;
- two replay blocks per image;
- primary deadline 95 ms;
- five outer folds;
- validation fold = (test+1) mod 5;
- training = remaining three folds.

No new request split or replay assignment.

## Direct-utility target

For each request:

`U = G * Z`.

Both real-data ablation models predict this exact same target.

## Common feature set

Image-side:
- local confidence;
- log payload bytes;
- training-only local-predicted-class benefit prior.

Network-side:
- log payload bytes;
- previous throughput;
- previous RTT;
- observation age;
- past-only 1-s EMA throughput;
- past-only 1-s EMA RTT;
- history count;
- cold start;
- operator;
- drive.

Current throughput, current RTT, realized service, realized deadline success, remote correctness and realized benefit are not features.

The payload feature is intentionally shared by both groups because payload is the measured bridge between request content and transport cost.

## Model architecture

Both models use the exact same `HistGradientBoostingRegressor` settings:
- loss = squared_error;
- learning_rate = 0.05;
- max_iter = 150;
- max_leaf_nodes = 15;
- min_samples_leaf = 50;
- l2_regularization = 1.0;
- early_stopping = False;
- identical fold-specific random_state.

### Interaction-OFF direct utility model

Same HGBR with interaction constraints:
- image group = {local confidence, log payload, predicted-class benefit prior};
- network group = {log payload, previous throughput, previous RTT, age, EMA throughput, EMA RTT, history count, cold start, operator, drive}.

Cross-side interactions are prohibited; payload is allowed to participate in both groups.

### Interaction-ON direct utility model

Same HGBR, same features, no interaction constraint.

## Budgets

Evaluate the already frozen rates:
- 10%;
- 25%;
- 50%.

Primary = 50%, because R3B selected 50% in every validation fold.

At each pair × fold × rate, both models offload exactly the same top-K request count.

No new rate selection occurs in R5A.

## Primary real-data estimand

`Delta_interaction = Accuracy_ON - Accuracy_OFF`.

Report pair-specific paired two-way image × trace-block bootstrap 95% CIs with 2000 replicates.

This is the clean interaction-value sensitivity. It does not replace R3B's factorized-vs-joint confirmatory result.

## Positive-control detectability experiment

A deliberately strong, known cross-side interaction is injected **only into a synthetic diagnostic target**, not into the real endpoint.

Within each outer fold, training rows determine:
- median local confidence;
- median non-missing previous throughput.

Define:
- `A = +1` for local confidence <= training median, else -1;
- `B = +1` for previous throughput <= training median, else -1; cold-start rows use 0.

Synthetic utility:

`U_PC = U + 0.25 * A * B`.

Both interaction-OFF and interaction-ON models are retrained on `U_PC` with otherwise identical settings.

Positive-control primary budget = 50%.

Detectability gate:
- joint interaction-ON gain over interaction-OFF >= +2.0 pp; and
- paired 95% CI lower bound > 0.

This positive control is intentionally stronger than the real effect and is used only to verify that the design/model/folds can recover a materially important cross-side interaction when one is present.

## Interpretation

- If the real interaction-ON minus interaction-OFF gain remains small while the positive control passes, the manuscript can state that the evaluation is capable of detecting a material cross-side interaction but finds little operational value for such interaction on the real replay.
- If the positive control fails, the real negative/near-equivalence interaction result must be described as potentially detectability-limited.
- No SESOI/equivalence rule is changed.
- No Glasgow result is used in R5A.
