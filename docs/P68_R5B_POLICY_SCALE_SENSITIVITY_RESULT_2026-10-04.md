# P68-R5B policy-scale sensitivity result

Date: 2026-10-04
Status: PASS — scale characterized; narrower-margin sensitivity materially refines the interpretation.

R5B reused the valid R3B held-out scores without retraining. It evaluated pre-specified 10%, 25%, 50% budgets and exploratory 60%, 75%, 90% budgets.

At the pre-specified 50% budget, Pair A joint-minus-factorized = +0.3735 pp, 95% CI [+0.2472,+0.5158], with 2.5929 pp remaining factorized-to-oracle headroom; the joint model recovers 14.40% of that headroom (bootstrap 95% CI 9.99%–19.11%). Pair B = +0.5775 pp, CI [+0.4078,+0.7510], with 3.2367 pp headroom; recovered fraction 17.84% (13.16%–22.18%).

Across the original 10/25/50% rates, every 95% CI lies wholly inside ±1 pp and ±2 pp, but none lies wholly inside ±0.5 pp or ±0.25 pp. Therefore the original ±2 pp confirmatory equivalence result is robust to a ±1 pp descriptive sensitivity, but not to materially tighter ±0.5/±0.25 pp margins.

Exploratory higher budgets show the joint advantage peaks around the middle budgets and collapses by 75–90%. At 75%, both pairs have CIs wholly inside ±0.25 pp; at 90% the joint model is slightly worse than factorized in both pairs (A -0.0400 pp, B -0.0381 pp).

The 50% boundary therefore did not conceal a growing joint advantage at higher offload rates. However, the reviewer is correct that the ±2 pp margin is permissive relative to available oracle headroom. The manuscript should retain ±2 pp only as the frozen confirmatory criterion and report the ±1/±0.5/±0.25 sensitivity plus oracle-headroom fractions prominently.