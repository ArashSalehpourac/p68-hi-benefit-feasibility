# P68-R3C — Fixed-budget robustness result

Date: 2026-10-04  
Status: **PASS — R3B equivalence conclusion is budget-robust**

R3C reused the stored held-out R3B OOF scores with no model retraining and no new budget. The frozen offload rates were 10%, 25%, and 50%.

## Pair A

- 10%: joint - factorized = **+0.2890 pp**, 95% CI **[+0.0370,+0.5350] pp**
- 25%: **+0.3215 pp**, 95% CI **[+0.0733,+0.5511] pp**
- 50%: **+0.3735 pp**, 95% CI **[+0.2447,+0.5191] pp**

## Pair B

- 10%: **+0.2792 pp**, 95% CI **[-0.0519,+0.6018] pp**
- 25%: **+0.4179 pp**, 95% CI **[+0.0727,+0.7658] pp**
- 50%: **+0.5775 pp**, 95% CI **[+0.4086,+0.7544] pp**

Every one of the six fixed-rate confidence intervals lies wholly within the original frozen **[-2,+2] pp** margin.

Tail differences remain small. At 10% and 25%, tail intervals include zero in both pairs; at 50%, tail gains are positive but remain far below the frozen materiality requirement already evaluated in R3B.

## Interpretation

The joint model's small advantage is not an artifact of the validation procedure choosing the 50% operating point. Across all three pre-specified offload rates, the joint-minus-factorized difference remains well below the 2-pp minimally important difference.

R3C is a secondary sensitivity analysis only. It does not replace or re-open the R3B confirmatory result.
