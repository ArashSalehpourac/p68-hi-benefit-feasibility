# P68-R6A — Service-round policy uncertainty sensitivity

Date: 2026-10-05  
Status: **PASS — RESULTS READY FOR MANUSCRIPT**

## Purpose

Close the post-review uncertainty asymmetry between the three-way mechanism robustness analysis and the headline two-way policy bootstrap, without reopening the frozen confirmatory analysis.

## Frozen inputs and scope

- Confirmatory R3B trained models, held-out rankings, folds, replay assignments, and validation-selected 50% boundary selections are reused unchanged.
- No policy model is retrained.
- Primary deadline: 95 ms.
- Five sustained-warm remote-service measurement rounds.
- The archived pooled payload-decile empirical service CDF was reconstructed exactly from the frozen JPEG service corpus; maximum absolute error versus stored q-star = 0.
- This is an **evaluation-side service-measurement sensitivity**. It does not claim model-refit sensitivity to alternative service-round training targets.

Source SHA-256:
- R3B held-out policy rows: `96213eb8430031be68191bf1c90bda7d5a24a7bc710959af0bd85cce1bdd4c82`
- PAM trace: `270194e69c6b68b487d4529a9cf648a66a347e62393964c9119ff971b1658194`
- sustained-warm service corpus: `bb5f71414744b125345ebb7a195e82ffaa481b935d67f86f44a06a3a0cbcd869`
- frozen inference-side table: `d1084d9d1308aeee10b55fc8ab80c982a9a980020ad3eedcf4563d4c6e2f2dd9`

## Service-round point sensitivity

Holding trained policies and selections fixed:

- Pair A joint−factorized contrast across rounds: **+0.3695 to +0.3873 pp**.
- Pair B: **+0.5604 to +0.5815 pp**.

For reference, the original realized-binary R3B effects are +0.3735 pp and +0.5775 pp.

## Three-way bootstrap

2,000 replicates independently resample:
1. image ID,
2. measured trace block,
3. service measurement round.

Seeds: 6870 (A), 6871 (B).

- Pair A: mean +0.3780 pp; **95% CI [+0.2522,+0.5183] pp**.
- Pair B: mean +0.5732 pp; **95% CI [+0.3963,+0.7487] pp**.

Both intervals remain positive and wholly inside the original prespecified ±2-pp operational margin.

## Worst-class-tail sensitivity

Using the frozen tail definitions and frozen factorized-to-oracle headroom:

- Pair A: three-way 95% recovery interval **[1.46%,17.30%]**.
- Pair B: **[1.01%,18.36%]**.

Both upper bounds remain below the frozen 20% material-tail rule.

## Decision

The service-round policy sensitivity **preserves the original operational interpretation**. Finite service-measurement sampling does not materially alter the joint−factorized contrast or the frozen tail decision under the evaluation-side sensitivity.

## Artifact hashes

- `R6A_SERVICE_ROUND_POLICY_SENSITIVITY.csv`: `19a1d7954312eda752e58323a95e8fb9b4f68d7e0f3540d410ae9aed594f1d61`
- `R6A_THREE_WAY_BOOTSTRAP_SUMMARY.csv`: `53cf5867556fd3e3b8c618218bb922adb8ef8b06c4745ad4341f195ac3bb92fc`
- `R6A_DECISION.json`: `b9319b7b1a9716f04312430285d76fc1a31575fdb6762852da462de042de4853`
- `README.md`: `ef1c90658d555b21d0f03409c4595c9780a847c95cdcac0e791f6000a2fc427b`
