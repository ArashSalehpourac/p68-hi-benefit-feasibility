# P68-R6A — Post-review service-round policy uncertainty sensitivity

Date: 2026-10-05  
Status: **PASS — scale interpretation unchanged**

## Purpose

A referee identified an uncertainty asymmetry: the mechanism robustness analysis resampled remote-service measurement rounds, while the headline policy comparison used the pre-specified paired two-way image-ID × trace-block bootstrap. R6A addresses that point without reopening the confirmatory analysis.

## Frozen inputs and non-changes

- PAM deadline: 95 ms.
- Held-out factorized/joint policy scores and 50% top-K selections are reused unchanged.
- No model is retrained.
- No policy threshold, fold, margin, endpoint, or confirmatory decision rule is changed.
- The same model-specific JPEG payload-size-decile service construction is used.
- Five sustained-warm service rounds are treated as the finite service-measurement clusters.

Input SHA-256:
- R3B held-out policy rows: `96213eb8430031be68191bf1c90bda7d5a24a7bc710959af0bd85cce1bdd4c82`
- PAM trace: `270194e69c6b68b487d4529a9cf648a66a347e62393964c9119ff971b1658194`
- Sustained-warm service raw: `bb5f71414744b125345ebb7a195e82ffaa481b935d67f86f44a06a3a0cbcd869`

The stored empirical q-star values were reconstructed from the five-round payload-decile service CDF with maximum absolute error `1.14e-7`.

## Estimand and uncertainty

For each held-out row and each service round, deadline feasibility is recomputed from the empirical service CDF restricted to that round. The round-standardized point estimate averages the five round-specific expected deadline-success probabilities while keeping the frozen policy selections fixed.

A 2,000-replicate three-way sensitivity independently resamples:
1. image ID;
2. measured trace block;
3. service round.

Bootstrap seed: `6862`.

This is a post-confirmatory sensitivity. It supplements, but does not replace, the original two-way confirmatory bootstrap.

## Results

Pair A:
- original realized joint−factorized: **+0.3735 pp**;
- service-round standardized: **+0.3790 pp**;
- three-way 95% interval: **[+0.2437,+0.5231] pp**;
- individual service-round effects: **+0.3695 to +0.3873 pp**.

Pair B:
- original realized joint−factorized: **+0.5775 pp**;
- service-round standardized: **+0.5746 pp**;
- three-way 95% interval: **[+0.4003,+0.7609] pp**;
- individual service-round effects: **+0.5604 to +0.5815 pp**.

Both three-way intervals remain wholly inside ±1 pp and the original ±2-pp operational-equivalence margin. Neither lies wholly inside ±0.5 pp.

## Decision

Finite sustained-warm service-round sampling does **not** materially change the policy-scale interpretation. The referee-requested uncertainty sensitivity is therefore closed without changing the confirmatory result or claim boundary.
