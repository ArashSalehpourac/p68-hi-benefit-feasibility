# P68-R3 — Confirmatory policy benchmark specification (FROZEN BEFORE OUTCOMES)

Date: 2026-10-04  
Status: **FROZEN BEFORE R3 POLICY EXECUTION**

This specification operationalizes the already-frozen R3 SESOI/equivalence rule. No joint-vs-factorized policy outcome had been computed when this document was written.

## Primary setting

- codec: JPEG q75 only, because frozen P2 inference outcomes are JPEG-specific;
- primary E2E deadline: 95 ms;
- measured network: frozen PAM'25 joint UL+RTT trace;
- remote service: empirical sustained-warm R1N distribution;
- feasibility architecture: frozen raw causal logistic q-hat;
- image outcomes: frozen P2;
- model pairs: A and B, analyzed separately first.

## Replay and held-out dependence structure

- Five outer folds.
- Image fold: deterministic balanced permutation of the 10,000 P2 image IDs with seed 6830.
- Trace-block fold: exact R1K five-fold block assignment.
- Each image is replayed against **two** deterministic trace blocks from its own outer fold; all 26 conditions are retained.
- Outer test fold k contains only image IDs and trace blocks absent from training.
- Validation fold is (k+1) mod 5; training uses the remaining three folds.
- No IID request split.

## Decision-time observables

Image-side:
- local max confidence;
- log payload bytes;
- training-only predicted-class benefit prior based on the local predicted class.

Network-side:
- payload bytes;
- previous throughput;
- previous RTT;
- observation age;
- past-only 1-s-half-life EMA throughput;
- past-only 1-s-half-life EMA RTT;
- history count;
- cold start;
- operator;
- drive.

Current-row throughput, current-row RTT, realized service latency, realized deadline success, remote correctness, and realized benefit are forbidden policy features.

## Fixed model classes

Benefit model g-hat:
- `HistGradientBoostingRegressor`;
- learning_rate = 0.05;
- max_iter = 150;
- max_leaf_nodes = 15;
- min_samples_leaf = 50;
- l2_regularization = 1.0;
- random_state fixed by outer fold.

It predicts E[G | image-side observables].

Feasibility model q-hat:
- exact R1K/R1P raw-logistic causal architecture;
- C = 1.0;
- numeric median imputation + missing indicators + standardization;
- operator/drive one-hot encoding;
- no post-hoc calibration.

Joint model u-hat:
- same fixed `HistGradientBoostingRegressor` hyperparameters as g-hat;
- input = image-side + causal network-side observables;
- target = realized deadline-adjusted incremental utility `U = G * Z`.

No hyperparameter search is permitted in R3.

## Policies

- Local only: no offload.
- Confidence only: score = `1 - local_confidence`.
- Confidence + feasibility: score = `(1-local_confidence) * q_hat`.
- Factorized: score = `g_hat * q_hat`.
- Joint: score = `u_hat`.
- Oracle-q diagnostic: score = `g_hat * q_star`, where q-star may use current realized network state and is explicitly non-deployable.
- Oracle realized-benefit ceiling: score = realized `G * Z`, diagnostic only.

## Primary matched offload count

Candidate rates are frozen at **10%, 25%, 50%**.

Within each outer fold, choose the primary rate that maximizes **factorized-policy validation deadline-adjusted accuracy**; ties choose the smaller rate. The selected rate is then applied unchanged to the held-out fold.

All deployable policies in the held-out fold offload exactly the same top-K request count.

## Secondary byte-budget comparison

In each held-out fold, the factorized top-K policy defines the reference transmitted-byte total. Every other policy follows its score ranking and takes the longest prefix whose cumulative payload does not exceed that same byte budget.

## Endpoint

For request i:

`A_i(policy) = local_correct_i + offload_i * G_i * Z_i`.

Primary endpoint = mean `A_i`.

Tail endpoint follows the separately frozen worst-20%-of-classes rule.

## Uncertainty

Headline joint-minus-factorized accuracy uses a paired two-way cluster bootstrap over:
- image ID;
- trace block.

Bootstrap resamples the two dependence sources independently and applies multiplicative cluster weights to the fixed held-out policy decisions.

Primary bootstrap reps: 2000; seed 6831.

No IID request-level CI is a headline result.

## Confirmatory rule

Use `docs/P68_R3_SESOI_EQUIVALENCE_FREEZE_2026-10-04.md` exactly.

No policy architecture, candidate budget set, SESOI, equivalence margin, tail definition, or interpretation rule may be altered after R3 execution begins.
