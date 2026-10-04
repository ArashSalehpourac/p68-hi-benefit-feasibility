# P68-R5C multiway mechanism uncertainty

Date: 2026-10-04
Status: FROZEN BEFORE EXECUTION

Purpose: address the reviewer concern that R2/R4C class-cluster confidence intervals condition on the observed network trace and remote-service sample.

R5C re-estimates uncertainty for the primary factorization-gap estimand in both measured network families: PAM at 95 ms and Glasgow at 35 ms. It uses the frozen P2 JPEG-q75 workload and frozen R1N empirical JPEG service measurements.

Primary families: additive and reductive. Additive-without-impulse is a sensitivity.

The point estimand remains unchanged. For uncertainty, use a three-way cluster bootstrap with 2000 replicates and independent resampling of: (1) the 200 ImageNet classes; (2) measured network temporal blocks; and (3) the five sustained-warm remote-service measurement rounds. Each selected network block retains all of its rows. Each selected service round retains its complete matched JPEG service measurements and payload-decile structure. This preserves within-block and within-round dependence.

For transparency also report class-only and class×network-block bootstrap intervals using the same replicate count, so the incremental effect of network/service uncertainty is visible.

The factorization gap is linear in the empirical feasibility distribution. The implementation may therefore precompute class × network-block × service-round gap contributions and combine them exactly under the bootstrap weights. The point estimates must reproduce the previously frozen R2/R4C primary gaps to numerical tolerance before any interval is accepted.

No new scientific threshold is introduced. R5C is an uncertainty sensitivity and does not alter the frozen R3 policy criteria.