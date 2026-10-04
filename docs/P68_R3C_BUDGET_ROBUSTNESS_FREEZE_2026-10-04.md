# P68 R3C — pre-specified budget robustness

Date: 2026-10-04
Status: FROZEN BEFORE R3C EXECUTION

R3C is a secondary sensitivity analysis. It does not alter the valid R3B confirmatory verdict.

The candidate offload rates 10%, 25%, and 50% were frozen before R3B. R3C evaluates joint versus factorized policy performance at each of those three fixed rates using the already fitted held-out R3B OOF policy scores. No model is retrained and no new rate is introduced.

For each model pair and fixed rate, rank held-out requests by the stored factorized and joint scores, offload exactly the same top-K count, and compute deadline-adjusted top-1 accuracy at the frozen 95-ms deadline. Report joint-minus-factorized difference with the same 2000-replicate paired two-way image × trace-block bootstrap used in R3B.

Also report the worst-20%-class tail difference using the R3B fold-specific tail labels. This analysis is robustness only: the frozen ±2 pp equivalence margin and 20% tail rule are not re-tested as a new confirmatory family.