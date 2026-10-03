# P68-R1 trace candidate audit — 2026-10-03

Status: initial public-source verification; schema-level ingestion audit pending.

| Candidate | Measurement setting | Throughput | RTT/latency | Temporal/mobility value | License status | R1 role |
|---|---|---:|---:|---|---|---|
| NUWiNS SIGMETRICS 2026 drive tests | Alaska, Hawaii, mainland baseline; cellular + Starlink campaigns | Yes | Yes | Road-test traces; ping files expose RTT and concurrent smart-throughput in Alaska/Hawaii | Data CC BY 4.0; code MIT | **Preferred primary** |
| NUWiNS PAM 2025 multi-carrier | Three cross-US drives; AT&T/T-Mobile/Verizon | Yes | Yes | Mobile throughput plus timestamp-processed RTT; route/operator structure | CC0-1.0 | **Preferred independent replication** |
| TU Wien SA-5G | Private standalone 5G, 7 fixed indoor locations | Yes | Yes | 60 s trials, 1 s reporting; throughput and latency campaigns separate | Data CC BY 4.0; code MIT | Controlled secondary arm |
| NYU-METS | NYC LTE bus/subway/ferry/car/rail | Yes (1 s TCP throughput) | Not verified in project audit | Long mobility throughput traces | ODbL 1.0 + DbCL 1.0 | Throughput-only backup |

## Mandatory ingestion checks

For each selected family record:
- exact upstream commit/release/DOI;
- file hashes;
- dataset license text;
- file list used;
- route / day / operator / run identifiers;
- timestamp timezone and resolution;
- throughput direction and unit;
- RTT field and whether measured concurrently with throughput;
- missing-value and zero/no-service semantics;
- interpolation/hold rule used by replay;
- block unit used for resampling;
- exclusions with reasons.

No dataset is admitted into confirmatory R2/R3 merely because it is public.
