# P68-R2 — Measured-network coupling and factorization result review

Date: 2026-10-04
Status: **RESULTS REVIEWED / INTERACTION OPERATIONALLY NEGLIGIBLE IN R2**

## Scope

R2 is the first phase that exposed the frozen historical P2 inference-side benefit outcomes. The primary benefit analysis is JPEG q75 only, matching the codec used to generate the frozen P2 remote predictions.

Primary deadline: 95 ms. Robustness window: 70–120 ms.

Benefit: `G = 1[remote correct] - 1[local correct]`.

Feasibility: exact empirical `qbar*` marginalized over the measured PAM UL+RTT trace and the empirical sustained-warm R1N service distribution, conditional on payload-size decile.

Primary factorization estimand is within `class × corruption × severity` strata.

## Primary 95-ms results

- Pair A / additive: within correlation +0.011557; factorization gap +0.006495 pp; class-bootstrap 95% CI +0.001086 to +0.011830 pp.
- Pair A / reductive: within correlation -0.018138; factorization gap -0.012572 pp; 95% CI -0.021355 to -0.003596 pp.
- Pair B / additive: within correlation -0.008563; factorization gap -0.004333 pp; 95% CI -0.009978 to +0.001760 pp.
- Pair B / reductive: within correlation -0.029949; factorization gap -0.017780 pp; 95% CI -0.025455 to -0.010257 pp.

Additive sensitivity excluding impulse noise remains tiny:
- A: +0.009547 pp;
- B: -0.006695 pp.

## Robustness over the frozen 70–120-ms window

Across the two primary families and both pairs, the largest absolute within-stratum factorization gap is only **0.023128 percentage points** (Pair B / reductive at 75 ms).

Relative to the deadline-adjusted remote-benefit increment, the factorization gap never exceeds approximately **0.29%** over the full deadline grid.

Network-stratum sensitivity preserves the same pair/family directions and remains tiny across all six operator×drive strata.

## Scale separation

R2 strengthens the distinction between aggregate association and request-level conditional coupling.

At 95 ms, pooled and between-condition-cell correlations can be materially larger than the within-stratum correlations. For example, Pair B / additive has pooled `Corr(G,qbar*) = -0.0807` and between-cell correlation `-0.5941`, while the within-stratum correlation is only `-0.00856` and the factorization gap is `-0.00433 pp`.

Thus aggregation can produce visually/nominally strong association without a material request-level interaction term.

## Directional mechanism

The original directional rule is not rescued by measured replay. Stratum-level expected-sign match shares are:
- A/additive 48.1%;
- A/reductive 43.3%;
- B/additive 54.5%;
- B/reductive 40.4%.

Only B/additive is slightly above chance and its class-bootstrap 95% CI for the gap includes zero.

## Realized-request replay

The 20-replicate realized replay produces raw request-level G–Z correlations very close to zero. Because the exact factorization gaps are on the order of hundredths of a percentage point, the 20-replicate Monte Carlo replay is too noisy to estimate those tiny gaps precisely and is retained as a qualitative validation only, not headline inference.

## Scientific conclusion

Measured network and service dynamics do **not** create a practically meaningful within-stratum benefit–feasibility interaction in R2. The observed interaction terms are statistically detectable in some cells but operationally negligible.

This result supports proceeding to the R3 policy benchmark as a direct test of whether a factorized policy is operationally equivalent to a flexible joint policy.

R3 must not run until the SESOI/equivalence rule is explicitly author-confirmed and frozen.