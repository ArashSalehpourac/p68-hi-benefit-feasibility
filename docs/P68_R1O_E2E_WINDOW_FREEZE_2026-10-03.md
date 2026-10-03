# P68-R1O — Outcome-blind end-to-end deadline-window freeze

Date: 2026-10-03
Status: **FROZEN — GLOBAL E2E WINDOW 70–120 ms**

## Inputs

R1O combined:
- frozen PAM'25 measured UL+RTT trace;
- frozen P0 payload distributions;
- full empirical sustained-warm R1N model×codec service distributions.

No inference benefit G, correctness, confidence, prediction, or policy endpoint was loaded.

## End-to-end construction

`L_e2e = RTT + serialization(payload, measured UL throughput) + remote_service`

Remote service was represented empirically rather than by one fixed p95 constant. Two service constructions were required simultaneously:
- marginal model×codec empirical service distribution;
- payload-size-decile-matched empirical service distribution.

No synthetic FIFO was used.

## Frozen non-saturation gate

A deadline is admissible only when expected feasibility is within [0.20, 0.80] under all of:
- trace-row weighting;
- equal frozen 2-s block weighting;
- equal operator×drive stratum weighting;

and under both service-distribution constructions.

At least three consecutive 5-ms deadlines were required.

## Results

Arm-specific admissible windows:
- Pair A / JPEG: 70–130 ms;
- Pair A / WebP: 70–125 ms;
- Pair B / JPEG: 65–120 ms;
- Pair B / WebP: 65–120 ms.

Pair-common windows:
- Pair A: 70–125 ms;
- Pair B: 65–120 ms.

The intersection across all four pair×codec arms is:

**70–120 ms**

Therefore the global common E2E window passes and is frozen at 70–120 ms.

## Primary operating point

The outcome-blind midpoint of the frozen global window is **95 ms**. Freeze 95 ms as the primary operating deadline for subsequent q-hat and policy analyses. The full 70–120 ms window remains a pre-specified robustness range.

At 95 ms under the marginal service construction, aggregate feasibility is:
- Pair A / JPEG: row 0.6088, block 0.5769, stratum 0.5964;
- Pair A / WebP: row 0.6159, block 0.5858, stratum 0.6015;
- Pair B / JPEG: row 0.6690, block 0.6403, stratum 0.6609;
- Pair B / WebP: row 0.6776, block 0.6508, stratum 0.6675.

Condition- and block-level heterogeneity remains substantial; some conditions and blocks are locally near saturation. Thus 70–120 ms is an **aggregate support window under the frozen gate**, not a claim that every condition or temporal block is individually non-saturated.

## Next step

Before loading inference benefit G, instantiate and audit the already-frozen raw-logistic causal q-hat architecture for end-to-end feasibility over the frozen 70–120 ms E2E window, with 95 ms primary.