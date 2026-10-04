# P68-R4B — Glasgow causal q-hat audit result

Date: 2026-10-04
Status: **FAIL — DO NOT FREEZE GLASGOW POLICY REPLICATION**

R4B executed cleanly with the frozen Glasgow trace, P0 payloads, R1N service samples and leave-one-date-out evaluation. No inference benefit/correctness/confidence or policy outcome was loaded.

All six pair×deadline cells fail the pre-specified discrimination/skill gate. Pair A AUCs are 0.5466, 0.5192, 0.5076 at 30/35/40 ms; Pair B AUCs are 0.4997, 0.4840, 0.5046. Brier skill ranges from -0.0152 to +0.0051. Pooled q-star ECE10 remains <=0.0493 and worst provider×device q-star ECE10 <=0.1356, so the failure is predictability rather than calibration.

The Glasgow sessions are sparse stationary Speedtest observations rather than a dense mobility trace. Past-only network state is not sufficiently predictive of the next session for a deployable per-request q-hat under the frozen gate.

Decision: do not run a deployable factorized-vs-joint policy replication on Glasgow with this q-hat and do not post-hoc tune around the failure. Glasgow remains usable for a non-policy external-validity replication of the factorization mechanism using exact empirical q-bar marginalized over measured Glasgow network states and R1N service.