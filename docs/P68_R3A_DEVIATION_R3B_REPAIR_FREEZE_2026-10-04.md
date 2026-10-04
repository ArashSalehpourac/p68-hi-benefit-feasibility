# P68-R3A implementation deviation and R3B protocol-compliance repair freeze

Date: 2026-10-04  
Status: **R3A INVALID FOR CONFIRMATORY CLAIM; R3B REPAIR FROZEN BEFORE R3B OUTCOMES**

## 1. What R3A produced

The first R3 execution completed and, under the code that was run, returned operational-equivalence verdicts for both model pairs.

These numerical results are retained as an audit trail but are **not accepted as the confirmatory R3 result** because the implementation did not exactly match the pre-outcome frozen policy specification.

## 2. Frozen-spec deviation discovered during review

The pre-outcome specification at commit:

`7f299fedf792166e7c04ce17acd518b8f7f7dee0`

explicitly froze the following image-side observables:

- local max confidence;
- log payload bytes;
- **training-only predicted-class benefit prior based on the local predicted class**.

R3A implemented:

`BENEFIT_FEATURES = ["local_confidence", "log_payload_bytes"]`

and the joint model likewise omitted the training-only predicted-class benefit prior.

Therefore both `g_hat` and `u_hat` were fit with one frozen image-side observable missing.

This is a protocol implementation error, not a scientific result.

## 3. R3A numbers retained but non-confirmatory

R3A count-matched primary results were:

- Pair A: joint − factorized = +0.3823 pp; two-way cluster 95% CI +0.1884 to +0.5706 pp; tail recovered fraction 4.52%; code verdict operational equivalence.
- Pair B: +0.5663 pp; 95% CI +0.3249 to +0.8129 pp; tail recovered fraction 4.87%; code verdict operational equivalence.

The paired CIs are inside the frozen [-2,+2] pp equivalence margin and the frozen 20% tail rule fails in both pairs. These values must be labeled **R3A implementation-deviation results** and cannot serve as the manuscript's confirmatory R3 evidence.

## 4. R3B repair frozen now

R3B changes **one protocol-compliance item only**:

For each pair and outer fold:

1. use training rows only;
2. compute `E[G | local_predicted_class]` by grouping training `G` on the frozen local model's predicted class;
3. use the training-wide mean `G` as fallback for any predicted class absent from training;
4. map that prior unchanged to training, validation, and held-out test rows;
5. include the resulting numeric `pred_class_benefit_prior` in both:
   - the fixed `g_hat` HGBR feature set;
   - the fixed joint `u_hat` HGBR feature set.

No other element may change.

Specifically unchanged:

- frozen SESOI/equivalence rule;
- 95-ms primary deadline;
- JPEG q75 scope;
- five outer image/trace folds;
- two deterministic replay blocks/image;
- validation-fold definition;
- HGBR hyperparameters/seeds;
- frozen raw-logistic q-hat;
- candidate rates 10%, 25%, 50%;
- factorized-only validation budget selection;
- matched-count primary comparison;
- matched-byte secondary comparison;
- worst-20%-class tail definition;
- 2000-replicate paired two-way image × trace-block bootstrap;
- interpretation rule.

## 5. Sequential-design status

The repair is dictated exactly by the pre-outcome frozen specification and is frozen before R3B outcomes are computed. No R3A result is used to tune the repair.

R3B will be the confirmatory R3 analysis if and only if its execution matches this repair record and the original frozen specification.
