# P68 R6 — Major-review revision freeze

Date: 2026-10-05
Status: INTERIM REVIEW REVISION — NOT SUBMISSION-READY

The independent review of the Computer Networks manuscript returned a Major Revision recommendation. Text/provenance corrections have been applied in manuscript v6.3 and supplement v6.3, but the scientific revision remains open until the analyses below are executed.

## Closed in v6.3

- Explicitly define the deployable q-hat training response as realized binary deadline success Z, using the frozen deterministic payload-decile-matched empirical service-latency realization (seed 6817). Exact empirical q-star remains the probability/calibration reference rather than the logistic-regression response.
- State that all validation folds selected the upper boundary (50%) of the prespecified 10/25/50% grid; 50% is not an estimated optimal offload rate.
- Tighten positive-control interpretation to the form and magnitude actually injected.
- Report absolute worst-class-tail accuracies, recoverable headroom, recovered fractions, and uncertainty.
- Remove reader-facing internal stage labels such as P2/R3B/R5B where they are not needed scientifically.
- Harmonize the PAM additive mechanism value to +0.00650 pp.
- Clarify that the preliminary simulation was earlier unpublished project analysis.
- Separate research-process AI assistance in Methods from manuscript-preparation AI disclosure.
- Remove superseded embedded manuscript PNG assets; exactly four active figures remain.

## R6A — Policy service-round uncertainty sensitivity

Purpose: answer the reviewer's concern that finite remote-service measurement uncertainty is propagated for the mechanism endpoint but not the headline policy endpoint.

Freeze:
- Do not retrain or re-rank any policy model.
- Reuse the valid held-out confirmatory policy scores, fixed offload masks, image folds, trace-block assignments, and original selected 50% budgets.
- Use the five frozen sustained-warm service-measurement rounds.
- Recompute realized deadline success under service-round resampling without changing the frozen E2E latency semantics.
- Primary uncertainty: paired cluster bootstrap over image ID × trace block × service round, 2,000 replicates.
- Report joint-minus-factorized deadline-adjusted accuracy and 95% CI for both pairs; also report worst-20%-class tail recovery.
- The original ±2 pp equivalence margin and 20% tail-materiality rule remain unchanged and are not reopened.

## R6B — Benefit-only g-hat policy ablation

Purpose: quantify the marginal contribution of feasibility after learned benefit is available.

Freeze:
- Use the existing out-of-fold g_hat values; no model retraining or hyperparameter change.
- Rank requests by g_hat only, using the same deterministic row-ID tie rule.
- Primary comparison uses the existing selected 50% matched-count budget.
- Report deadline-adjusted accuracy for both model pairs and difference versus factorized g_hat*q_hat.
- Optionally report the already frozen 10/25/50% rates descriptively.
- This is a post-review ablation, not a reopened confirmatory test.

## R6C — Pinned-environment replication

Purpose: address the missing original scikit-learn version.

Freeze:
- The exact original scikit-learn version is not claimed recovered unless documented by an archived environment artifact.
- Rerun the critical q-hat audit and matched-capacity interaction ON/OFF analysis in a newly pinned environment.
- Archive Python version, scikit-learn version, pandas/NumPy/PyArrow versions, full pip freeze or lockfile, and execution hashes.
- Confirm the q-hat gate verdict and primary interaction effects reproduce to a declared numerical tolerance before calling the provenance issue closed.
- No scientific threshold, fold, endpoint, or interpretation criterion may be changed.

## Current revision artifacts

- Main: P68_Computer_Networks_REVIEW_REVISION_v6_3.docx
  - SHA-256: 99d4ccf37b4192487d6fd9a16a09c070bfec8663eefb6e493647f15a53bb17f5
  - Drive ID: 1P7hwv1OigBbVXt5zWU4yIJzttNTPRPvb
- Supplement: P68_Computer_Networks_SUPPLEMENTARY_INFORMATION_REVIEW_v6_3.docx
  - SHA-256: 915fa42163381e9557039de9144774ac3e17a7a1354ffe57e4098fa37f71d08d
  - Drive ID: 1H9yMAaIpkvUHOPJx8owhNB_wpGtY_1a_

QA: main 16 rendered pages; supplement 8 rendered pages; accessibility clean; no comments/tracked changes; main contains exactly four active figure assets.

Do not rebuild a final submission package until R6A is completed and reviewed. R6B and R6C should also be completed if feasible because they directly answer the reviewer's requested ablation/provenance concerns.
