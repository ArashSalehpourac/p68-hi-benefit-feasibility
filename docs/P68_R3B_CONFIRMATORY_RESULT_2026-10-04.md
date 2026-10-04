# P68-R3B — Confirmatory factorized-vs-joint policy result

Date: 2026-10-04  
Status: **VALID CONFIRMATORY RESULT — OPERATIONAL EQUIVALENCE IN BOTH MODEL PAIRS**

## Sequential integrity

R3B is the protocol-compliance rerun frozen at commit:

`0409b0dc36109e55a02e2fd3e6acd8e4991efbe6`

before R3B outcomes were computed.

The R3A run remains non-confirmatory because it omitted one image-side observable already frozen in the pre-outcome specification. R3B restores exactly that feature: the training-only local-predicted-class benefit prior. No SESOI, margin, model hyperparameter, fold, replay, budget, bootstrap, endpoint, or interpretation rule was changed.

R3B execution integrity:
- no notebook execution errors;
- P2 / trace / service / R1K-fold hashes matched;
- frozen-spec compliance assertions passed;
- 10,000 images;
- 344 trace blocks;
- 20,000 image×block cells;
- zero train/test image overlap;
- zero train/test trace-block overlap;
- 2,000 two-way image×trace-block bootstrap replicates.

## Frozen primary setting

- JPEG q75;
- 95-ms E2E deadline;
- same held-out offload count;
- candidate rates 10%, 25%, 50%, selected using factorized validation accuracy only;
- all ten pair×outer-fold validations selected 50%.

## Primary confirmatory result

### Pair A — MobileNetV3-Small -> ConvNeXt-Base

- Factorized deadline-adjusted accuracy: **43.8231%**
- Joint deadline-adjusted accuracy: **44.1965%**
- Joint - factorized: **+0.3735 pp**
- paired two-way cluster 95% CI: **[+0.2440, +0.5136] pp**

Worst-20%-class tail:
- factorized: **28.5919%**
- joint: **28.7922%**
- oracle realized ceiling: **30.7471%**
- joint tail gain: **+0.2003 pp**
- tail-gain 95% CI: **[+0.0343, +0.3762] pp**
- recoverable-tail fraction: **9.29%**

Frozen verdict: **OPERATIONAL EQUIVALENCE**.

### Pair B — ResNet18 -> ViT-B/16

- Factorized deadline-adjusted accuracy: **45.1194%**
- Joint deadline-adjusted accuracy: **45.6969%**
- Joint - factorized: **+0.5775 pp**
- paired two-way cluster 95% CI: **[+0.4161, +0.7510] pp**

Worst-20%-class tail:
- factorized: **28.5678%**
- joint: **28.8404%**
- oracle realized ceiling: **31.3823%**
- joint tail gain: **+0.2727 pp**
- tail-gain 95% CI: **[+0.0099, +0.5141] pp**
- recoverable-tail fraction: **9.69%**

Frozen verdict: **OPERATIONAL EQUIVALENCE**.

## Interpretation under the frozen rule

The joint policy is statistically detectably better than the factorized policy in both pairs, because the paired 95% CIs are entirely above zero.

However, the gains are **far below the frozen +2.0-pp SESOI** and their confidence intervals lie wholly inside the frozen **[-2,+2] pp equivalence margin**.

The class-tail gain is also positive but recovers only ~9-10% of oracle headroom, below the frozen 20% material-tail requirement.

Therefore the correct confirmatory interpretation is:

> A flexible joint interaction model yields a small positive gain, but that gain is operationally equivalent to the factorized policy under the pre-specified margin in both model pairs.

This is not a claim of exact equality or zero interaction.

## Secondary matched-byte result

At the same transmitted-byte budget:

- Pair A: factorized 43.8231%, joint 44.1148% -> **+0.2917 pp**
- Pair B: factorized 45.1194%, joint 45.6090% -> **+0.4896 pp**

The secondary result agrees directionally with the primary conclusion.

## Architectural value

The factorized policy substantially outperforms simpler confidence-based baselines while remaining close to the flexible joint model.

At matched count:
- Pair A: confidence×qhat 41.9437%, factorized 43.8231%, joint 44.1965%.
- Pair B: confidence×qhat 42.1333%, factorized 45.1194%, joint 45.6969%.

Thus the result is not “all policies are the same.” The evidence specifically supports the value of modeling inference benefit and feasibility while showing little operational value from learning their interaction jointly in this setting.

## Study-level label

**EQUIVALENCE_BOTH_MODEL_PAIRS**

## Next scientific gate

The current confirmatory claim is supported on one admissible measured trace family (PAM'25), JPEG q75, two model pairs, 200 ImageNet classes, and synthetic corruption families.

Before making a broad cellular-network claim, proceed to external-validity expansion / independent measured-trace replication. Do not broaden the claim from this R3B result alone.
