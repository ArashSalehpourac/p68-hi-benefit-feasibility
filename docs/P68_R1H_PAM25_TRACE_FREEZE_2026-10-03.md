# P68 — PAM'25 Joint Trace Freeze (R1H)

**Date:** 2026-10-03  
**Status:** FROZEN FOR POST-REJECTION MEASURED-NETWORK REDESIGN  
**Branch:** `post-rejection-redesign`

## Decision

PAM'25 is admitted as P68's **primary joint measured-network trace** for the confirmatory redesign.

SIGMETRICS'26 Alaska remains useful as marginal/network-realism evidence but is not used as the confirmatory joint RTT+uplink trace because R1E found zero shared provenance at operator+run+segment+src_idx, operator+run+segment, and operator+run levels.

## Frozen PAM source

- Repository: `NUWiNS/pam2025-multi-carrier-dataset`
- Pinned commit: `782b712599f3710f7d3acff57097af6ca14660ae`
- License: CC0 1.0 Universal
- Drives: D2 and D3
- Operators: AT&T, T-Mobile, Verizon
- Direction: uplink
- Throughput field: `Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]`

## Frozen alignment semantics

- XCAL clock: released `TIME_STAMP`
- Alignment orientation: XCAL -> next RTT
- Direction: `forward`
- Tolerance: 100 ms
- Repeated RTT timestamps: one-to-one use; keep earliest matched XCAL row
- Joint sample time: matched RTT timestamp
- Genuine zero-throughput rows: retained
- Synthetic FIFO queue: prohibited for this measured-throughput trace

This mirrors the source repository's released RTT/XCAL alignment semantics. `GPS Time` is not used for RTT pairing; R1G showed an approximately one-hour offset from `TIME_STAMP` in most non-CST files.

## R1H admission evidence

- Usable RTT rows before pairing: 186,792
- Measured UL XCAL rows before pairing: 290,956
- Source-faithful joint rows: **6,184**
- RTT-reuse rows before de-duplication: **0**
- Duplicate XCAL timestamps in the measured-UL population: **0**
- Operator x drive strata: **6/6 non-empty**
- Joint rows by stratum:
  - AT&T D2: 505
  - AT&T D3: 1,622
  - T-Mobile D2: 546
  - T-Mobile D3: 1,473
  - Verizon D2: 524
  - Verizon D3: 1,514
- Source files contributing joint samples: **24/27**
- The three ordinary D2 day-4 files do not produce source-faithful joint matches; the three `*_cst_*` day-4 files do. No manual row substitution is performed.
- Zero-throughput joint rows retained: **121**
- Negative-throughput rows: **0**
- Alignment p95 by stratum: 85–100 ms

## Frozen canonical trace

File: `PAM25_CANONICAL_JOINT_UL_RTT_forward100ms.csv`

SHA-256:

`270194e69c6b68b487d4529a9cf648a66a347e62393964c9119ff971b1658194`

## Temporal blocks

Primary outcome-blind block definition: split within original source file whenever the gap between consecutive matched RTT timestamps exceeds **2.0 s**.

R1H gap diagnostics:
- median gap: 1.0 s
- p90: 1.6 s
- p95: 2.8 s

At the 2-s threshold:
- blocks: 344
- median block size: 20 rows
- p95 block size: 31 rows
- maximum block size: 60 rows
- singleton-block share: 6.69%

Sensitivity block definitions: 1 s and 5 s.

## Authorization

R1H authorizes **T6 only**: an outcome-blind deadline-window/saturation preflight using the frozen P0 payload sizes plus the frozen PAM joint trace.

T6 must not load benefit, correctness, confidence, or routing-policy outcomes.

Because PAM throughput is measured application throughput, it must not be interpreted as unused service capacity in a synthetic FIFO queue.