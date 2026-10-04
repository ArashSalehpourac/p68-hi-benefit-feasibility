# P68-R5B policy-scale sensitivity

Date: 2026-10-04
Status: FROZEN BEFORE EXECUTION

Purpose: address reviewer concerns about the ±2 pp equivalence margin and the original 50% budget boundary without reopening R3B.

Use only stored valid R3B held-out scores; do not retrain models.

Budgets: existing 10%, 25%, 50%; exploratory 60%, 75%, 90%, frozen now before execution. At each pair/fold/rate, evaluate factorized, joint and realized-utility ceiling at the same top-K count.

Report factorized, joint and ceiling accuracy; joint-minus-factorized difference; remaining ceiling headroom; fraction of remaining headroom recovered; paired two-way image × trace-block bootstrap 95% CIs for the difference and recovered fraction.

Margin sensitivity: report whether the joint-minus-factorized 95% CI lies wholly inside ±0.25, ±0.50, ±1.00, and ±2.00 pp. Only ±2.00 pp is the original frozen confirmatory margin; narrower margins are descriptive sensitivities.

Using the already frozen R3B worst-20%-class labels, also report tail accuracies, tail headroom, and recovered tail fraction. No new tail threshold is introduced.

R3B remains the confirmatory analysis.