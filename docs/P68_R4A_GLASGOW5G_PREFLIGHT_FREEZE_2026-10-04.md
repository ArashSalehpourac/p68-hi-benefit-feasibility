# P68-R4A — Glasgow 5G outcome-blind trace-admission and E2E-window preflight (FROZEN BEFORE EXECUTION)

Date: 2026-10-04  
Status: **FROZEN BEFORE R4A EXECUTION**

R4A is an outcome-blind external-validity preflight. It must not load P2 inference benefit/correctness/confidence/policy outcomes.

## Source

- Zenodo record: `10.5281/zenodo.20465872`, version 2.
- Dataset file: `Glasgow5GDataSet.xlsx`.
- Expected MD5 from Zenodo: `375c58bd79d1e0762724fb78f67b4230`.
- License: CC BY 4.0.
- Expected raw sessions: 720.

## Canonical trace semantics

Use:
- upload speed as measured application uplink throughput;
- ping as measured RTT;
- timestamp as session time;
- provider, device and location as context.

Primary block:
`date × provider × device`.

Expected:
- 24 blocks;
- 30 sessions/block.

Sort by timestamp inside each block.

No synthetic FIFO.

## E2E construction

`L_e2e = ping + 8*payload_bytes/(1000*upload_mbps) + remote_service`.

Remote service uses the frozen empirical R1N sustained-warm JPEG distributions.

Payloads use the frozen outcome-free P0 JPEG-q75 primary subset.

No P2 file may be loaded in R4A.

## Fixed deadline grid

Scan absolute E2E deadlines:

**20, 25, 30, ..., 120 ms**.

## Service-distribution constructions

Both are required:
1. marginal empirical model×JPEG service distribution;
2. payload-size-decile matched empirical model×JPEG service distribution.

## Non-saturation gate

For each pair and deadline, feasibility must be inside **[0.20,0.80]** simultaneously under:
- empirical row weighting;
- equal 24-block weighting;
- equal provider weighting;

and under both service constructions.

An arm has an admissible window only if at least **3 consecutive 5-ms grid points** pass.

A global common window exists only if both model pairs pass on the same >=3 consecutive grid points.

If multiple global windows exist:
1. choose the longest;
2. tie -> choose the earlier window.

Primary Glasgow deadline = grid point nearest the selected window midpoint; exact midpoint ties choose the earlier grid point.

If no global common window exists, report pair-specific windows but do not claim common-deadline replication.

## T7 reporting

At the selected midpoint, report:
- block feasibility p10/p50/p90;
- share of blocks with feasibility <0.05;
- share of blocks with feasibility >0.95;
- provider-level feasibility.

These diagnostics are reported but do not replace the frozen aggregate gate.

## Decision

PASS for R4B eligibility requires:
- source hash/schema validity;
- 720 canonical sessions;
- 24 expected temporal blocks;
- positive upload/ping;
- session-level joint upload+ping;
- at least one admissible pair window.

A global common window is preferred but not required for pair-specific replication.

No threshold may be altered after execution.
