# P68-R4A — Independent measured-trace candidate: Glasgow 5G Dataset 2025

Date: 2026-10-04  
Status: **CANDIDATE ADMITTED FOR OUTCOME-BLIND PREFLIGHT; R4 POLICY OUTCOMES NOT YET EXPOSED**

## Source

Dataset:
- Hart, A. *Glasgow 5G Dataset 2025*, Zenodo, version 2.
- DOI: `10.5281/zenodo.20465872`
- license: **CC BY 4.0**
- primary file: `Glasgow5GDataSet.xlsx`

Peer-reviewed descriptor:
- Hart, A., Sturley, H., Mclean, P., Salva-Garcia, P., Shakir, M. Z.
- *Glasgow Public and Private 5G Performance Dataset (2025): Acquisition and Comparative Analysis*
- Scientific Data (2026)
- DOI: `10.1038/s41597-026-07600-w`

## Verified dataset design

The released public-5G component contains:
- 720 measurement sessions;
- 15 Glasgow neighbourhoods;
- 3 collection days (6–8 April 2025);
- 4 providers: EE, Vodafone, O2, Sky Mobile;
- 2 devices: Samsung Galaxy S24 Ultra and Google Pixel 9 Pro;
- 2 data points per provider × device × location × day.

Each released row is a session-level mean of 5–10 consecutive Speedtest runs at the same location/provider/device/time slot.

Each session contains jointly reported:
- upload throughput;
- download throughput;
- ping/RTT;
- SS-RSRP;
- timestamp;
- location;
- provider;
- device.

The paper states that each session was a full test cycle and the raw sheets contain the throughput and ping fields in the same row.

## R4 role

This dataset is an **independent stationary urban public-5G trace family**, not a mobility trace. It may therefore support independent network-family external validity but must not be described as another mobility campaign.

For P68 offload replay:
- use **Upload Speed (Mbps)** as measured application uplink throughput;
- use **Ping (ms)** as measured RTT;
- no synthetic FIFO;
- remote service remains a separately identified empirical component.

## Pre-outcome R4A block definition

Primary temporal block:
`date × network_provider × test_device`.

Expected:
- 3 dates × 4 providers × 2 devices = **24 blocks**;
- 15 locations × 2 sessions = **30 rows/block**.

Rows are sorted by timestamp within each block.

This preserves provider/device/day temporal order while allowing location to change as it did during the measurement campaign.

## Admission status before execution

- T1 license: **PASS** from Zenodo/descriptor (CC BY 4.0).
- T2 provenance: **PASS provisionally**; schema/hash will be verified by R4A.
- T3 temporal fidelity: **PENDING R4A canonicalization**.
- T4 block definition: **FROZEN above before outcome exposure**.
- T5 jointness: **PASS at session level** for upload/ping in the released Speedtest row.
- T6 informative E2E window: **PENDING R4A outcome-blind audit**.
- T7 saturation: **PENDING R4A**.

## Scope guardrail

R4A loads no inference benefit, correctness, confidence, joint-policy, or factorized-policy outcome. It only determines whether this independent trace family provides a non-saturated E2E regime for replication.

If R4A passes T6/T7, R4B may replicate the frozen factorized-vs-joint comparison on this trace family using a separately frozen causal feasibility protocol.

If R4A is saturated across plausible deadlines, the Glasgow dataset remains useful as external network-realism evidence but cannot serve as the independent confirmatory interaction replication.
