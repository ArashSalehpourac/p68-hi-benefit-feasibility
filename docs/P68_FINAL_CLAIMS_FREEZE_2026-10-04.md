# P68 — Final scientific claims freeze after R1–R4

Date: 2026-10-04  
Status: **CLAIMS FROZEN FOR MANUSCRIPT REBUILD**

## Primary claim

Under measured network dynamics, substantial aggregate or regime-level benefit–feasibility association does not imply a practically meaningful request-level interaction term.

## Mechanism evidence

The within-stratum factorization gap is operationally negligible in two independent measured network families:

1. PAM mobility trace:
   - primary 95-ms gaps range from about -0.0178 pp to +0.0065 pp;
   - maximum absolute gap over the full 70–120-ms robustness grid is about 0.0231 pp.

2. Glasgow stationary public-5G trace:
   - primary 35-ms gaps range from about -0.0031 pp to +0.0020 pp;
   - maximum absolute primary-family gap over 30/35/40 ms is about 0.0031 pp;
   - maximum absolute gap over all 24 Glasgow network blocks is about 0.0089 pp.

The original directional sign mechanism is not supported in either family.

## Deployable policy claim

On the PAM mobility family, a flexible joint policy is statistically better than the factorized policy but operationally equivalent under the pre-specified margin.

R3B:
- Pair A: +0.3735 pp, 95% CI [+0.2440,+0.5136] pp.
- Pair B: +0.5775 pp, 95% CI [+0.4161,+0.7510] pp.
- Both intervals lie wholly inside the frozen [-2,+2] pp equivalence margin.
- Recoverable worst-20%-class tail fractions are 9.29% and 9.69%, below the frozen 20% materiality requirement.

R3C shows this conclusion is robust across the pre-specified 10%, 25%, and 50% offload rates: all six fixed-rate confidence intervals remain wholly inside the original +/-2 pp margin.

## Glasgow scope restriction

Glasgow supports mechanism external validity only.

The frozen causal feasibility model failed leave-one-date-out discrimination on Glasgow:
- AUC approximately 0.484–0.547;
- Brier skill approximately -0.015 to +0.005.

Therefore do not claim deployable factorized-vs-joint policy equivalence on Glasgow.

## Architectural interpretation

The paper may claim that explicitly modeling benefit and feasibility is valuable, while learning an additional request-level benefit-feasibility interaction provides only a small operational gain in the PAM policy setting.

Do not claim:
- exact statistical independence;
- zero interaction;
- universal policy equivalence;
- equivalence across all cellular networks;
- Glasgow policy equivalence;
- causality of the observed aggregate associations.

## External-validity wording

Defensible:
- "replicated across a mobility trace and an independent stationary public-5G measurement family" for the mechanism result.

Not defensible:
- "replicated deployable policy equivalence across two networks."

## Manuscript consequence

The rejected simulator-only manuscript should be rebuilt around:
1. measured-network evidence;
2. aggregate-versus-request-level scale separation;
3. pre-specified factorization estimand;
4. matched-budget factorized-versus-joint policy equivalence on PAM;
5. independent Glasgow mechanism replication;
6. explicit failure of causal online feasibility prediction on sparse Glasgow sessions as a boundary condition.
