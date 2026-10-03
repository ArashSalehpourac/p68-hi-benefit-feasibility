# P68-R1J — Causal network observability audit

Date: 2026-10-03  
Status: **CAUSAL FEATURE RULE FROZEN; q-hat CALIBRATION MODEL NOT YET FROZEN**

## Purpose

Audit whether deadline feasibility can be estimated at decision time from strictly past-only network information, before loading any inference benefit, correctness, confidence, or policy outcome.

## Frozen causal feature rule

For request i, the routing policy may use:
- payload bytes;
- previous same-block measured uplink throughput;
- previous same-block measured RTT;
- age of the latest observation;
- past-only 1-s-half-life EMA throughput;
- past-only 1-s-half-life EMA RTT;
- history count / cold-start flag;
- operator and drive identity.

The current request's measured throughput and RTT are forbidden as policy inputs. They are used only to construct the network-only realization label Z_net.

Network dependence is split at the frozen 2-s temporal-block level, stratified by operator×drive. No request-level IID split is allowed.

## Observability results

Of 6,184 canonical trace rows, 5,840 (94.44%) have same-block history; 344 are conservative cold starts.

Overall:
- age p50 = 1,000 ms;
- age p95 = 1,800 ms;
- 89.78% of historical observations are <=1 s old;
- 100% are <=2 s old by construction;
- lag-1 throughput Spearman = 0.9437;
- lag-1 RTT Spearman = 0.6441;
- 1-s EMA throughput Spearman = 0.9364;
- 1-s EMA RTT Spearman = 0.6964.

All six operator×drive strata retain strong throughput persistence (lag-1 Spearman 0.885–0.949) and moderate-to-strong RTT persistence (0.501–0.693).

## Held-out feasibility-estimation audit

The audit used block-level 60/20/20 train/calibration/test splits and a pooled logistic estimator with isotonic calibration.

Across the frozen 60–110 ms network-component deadlines:

JPEG:
- held-out AUC: 0.8225–0.8627;
- Brier skill vs marginal: 0.2725–0.3893;
- overall ECE10: 0.0164–0.0479.

WebP:
- held-out AUC: 0.8285–0.8563;
- Brier skill vs marginal: 0.2858–0.3902;
- overall ECE10: 0.0202–0.0515.

Thus strictly causal past-only network features carry substantial predictive information.

## Important limitation

Pooled calibration is not uniformly calibrated by operator×drive. Worst-stratum ECE10 remains about 0.099–0.127 depending on codec/deadline, with the largest errors often in T-Mobile strata.

Therefore:
- the **causal observability semantics are frozen**;
- the simple pooled logistic + global isotonic q-hat specification is **not frozen** for R3;
- a network-only calibration repair must be completed before inference benefit outcomes are allowed into policy benchmarking.

This is nuisance-model development using network-only labels and does not alter the frozen T6 window or historical P2 benefit results.
