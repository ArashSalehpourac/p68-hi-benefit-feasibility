# P68-R5A — Matched-capacity interaction ablation result

Date: 2026-10-04  
Status: **PASS — MATERIAL INTERACTION DETECTABILITY CONFIRMED; REAL INTERACTION VALUE SMALL**

## Integrity

R5A executed cleanly from the frozen specification at commit:

`6a34e004ceebe1614679b0db0bb90bb73dbd2cb5`

Exact trace, service, P2 and fold hashes matched. The valid R3B image/trace replay structure was reused.

The real comparison used two direct-utility HGBR models with:
- identical target `U = G*Z`;
- identical features;
- identical training/test rows;
- identical folds;
- identical hyperparameters and random states;
- identical held-out top-K budgets.

The only intended difference was whether image-side × network-side cross-interactions were allowed.

## Real-data interaction value

### Pair A

- 10%: Interaction-ON − OFF = **+0.0694 pp**, 95% CI **[+0.0042,+0.1328] pp**
- 25%: **+0.1267 pp**, CI **[+0.0581,+0.1937] pp**
- 50% primary: **+0.1340 pp**, CI **[+0.0781,+0.1945] pp**

### Pair B

- 10%: **+0.0442 pp**, CI **[-0.0262,+0.1149] pp**
- 25%: **+0.1375 pp**, CI **[+0.0544,+0.2299] pp**
- 50% primary: **+0.1317 pp**, CI **[+0.0797,+0.1822] pp**

All six intervals lie entirely within the original ±2-pp operational-equivalence margin.

## Positive-control detectability

The frozen synthetic cross-side interaction used:

`U_PC = U + 0.25*A*B`

with training-only thresholds.

At the primary 50% budget:

- Pair A: Interaction-ON − OFF = **+4.4461 points**, 95% CI **[+4.0272,+4.8485]**
- Pair B: **+3.9335 points**, 95% CI **[+3.5269,+4.3726]**

Both pass the pre-specified positive-control gate:
- gain >= +2.0 points;
- CI lower bound > 0.

## Interpretation

R5A directly addresses the concern that R3B changed more than interaction flexibility.

Under a matched-capacity, same-target, same-feature direct-utility ablation, allowing image-side × network-side cross-interactions improves real deadline-adjusted accuracy by only about **0.13 pp** at the primary 50% budget.

The positive control shows that the same design, folds and model family can recover a deliberately material cross-side interaction when one is present.

Therefore the small real interaction gain is not plausibly explained solely by an inability of the evaluation to detect interactions of operationally material magnitude.

This remains a measured-network-replay result and does not establish arbitrary deployment-level independence.
