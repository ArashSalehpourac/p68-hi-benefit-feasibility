# P68-R1 measured-trace schema manifest (source-level audit)

Date: 2026-10-03
Status: source-level audit complete for two preferred families; row-level ingestion audit pending.

## Canonical replay schema

Every admitted trace row should be normalized to the following fields where supported:

| Field | Meaning |
|---|---|
| source_family | upstream dataset identifier |
| source_commit | pinned upstream commit |
| campaign | campaign / drive |
| operator | cellular operator |
| run_id | original run identifier |
| segment_id | route/run segment identifier if available |
| timestamp_s | monotonically ordered absolute or run-relative time |
| throughput_mbps | measured available/application throughput used by replay |
| throughput_direction | uplink/downlink |
| rtt_ms | measured RTT if available |
| tech | LTE / 5G-low / 5G-mid / 5G-mmWave / other if available |
| area | urban/rural/route label if available |
| is_joint | throughput and RTT measured/aligned for the same timestamped observation |
| missing_reason | explicit no-service / absent / invalid reason |
| source_file | original relative path |

Primary replay must preserve timestamp order inside each run/segment/operator block.

---

## A. NUWiNS SIGMETRICS 2026 drive-test artifact

Repository:
`NUWiNS/sigmetrics26-exploring-the-5g-digital-divide-in-the-non-contiguous-us-leo-satellites-to-the-rescue`

Pinned source commit for this audit:
`b5f330d508e08e8e1fcd2300529a45f1bbb3231d`

License:
- datasets: CC BY 4.0 (`LICENSE-DATA`)
- software/config: MIT

Release structure reported by upstream README:
- Alaska road test: 76 files, approx. 234 MB after extraction
- Hawaii road test: 115 files, approx. 185.2 MB
- LA→Omaha baseline: 20 files, approx. 282.8 MB
- tarballs are Git-LFS managed

Sampling / relevant subdirectories:
- Alaska/Hawaii XCAL: 500 ms
- Alaska/Hawaii application throughput: 500 ms
- Alaska/Hawaii ping: 200 ms
- LA→Omaha throughput: 500 ms
- LA→Omaha latency: 200 ms

Documented field mapping:

### Alaska/Hawaii `ping/<op>_ping.csv`
- `rtt_ms` → `rtt_ms`
- `operator` → `operator`
- `Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]` → candidate downlink `throughput_mbps`
- `Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]` → candidate uplink `throughput_mbps`
- XCAL/radio context is joined into the ping table according to upstream README
- **This is the preferred joint throughput+RTT source for the primary replay**, subject to row-level verification.

### Alaska/Hawaii `throughput/<op>_tcp_<dir>.csv`
- `time` → timestamp
- `throughput_mbps` → application throughput
- `retrans`, `cwnd_kb`, `weather`, `area` retained as optional diagnostics

### LA→Omaha
Throughput files expose:
- `utc_ts`, `local_dt`
- `run_id`, `segment_id`
- `dl_tput_mbps`, `ul_tput_mbps`
- `lat`, `lon`, `actual_tech`, `area`

Latency files expose:
- `utc_ts`, `local_dt`
- `rtt_ms`
- `run_id`, `operator`
- `lat`, `lon`, `speed_mph`, `actual_tech`, `segment_id`, `area`

LA→Omaha throughput and latency are separate file families; jointness must be established by timestamp/run alignment before using them as an empirical joint trace.

### Required row-level checks before admission
- verify monotonicity and duplicate timestamps;
- quantify missing/no-service samples;
- confirm whether concurrent throughput fields in ping files are raw, filtered, or padded;
- exclude or separately flag `is_padded=True` XCAL rows;
- identify exact downlink/uplink direction used by the HI replay;
- define hold/interpolation rule from 200/500 ms samples to request arrivals;
- define route/day/run/operator resampling block.

---

## B. NUWiNS PAM 2025 multi-carrier artifact

Repository:
`NUWiNS/pam2025-multi-carrier-dataset`

Pinned source commit for this audit:
`782b712599f3710f7d3acff57097af6ca14660ae`

License:
- CC0 1.0 Universal (`LICENSE`)

Campaign structure reported by upstream README:
- Drive 1: Boston→Los Angeles
- Drive 2: Boston→Atlanta
- Drive 3: Boston→Chicago
- operators: T-Mobile, Verizon, AT&T

Relevant repository structure:
- `datasets/raw_files/`
- `datasets/processed_files/extracted_tput_data/`
- `datasets/processed_files/extracted_ping_data/`
- `datasets/analysis_ready_files/rtt_aligned_tech/`
- `datasets/analysis_ready_files/throughput_analysis/`

Upstream processing documents:
- XCAL rows include `TIME_STAMP`, GPS, DL/UL throughput, technology/frequency fields and handover events.
- ping data are processed to obtain RTT timestamps.
- `merge_rtt_gps.py` merges RTT with XCAL by timestamps for technology-aligned RTT analysis.

Primary intended use:
- independent measured-mobility replication of the SIGMETRICS-family result;
- use only after exact RTT↔throughput timestamp alignment is verified at row level.

### Required row-level checks before admission
- enumerate actual files for each drive/operator/direction;
- verify timestamp domains used by XCAL and ping data;
- quantify alignment tolerance and unmatched rows;
- determine whether throughput and RTT are truly concurrent enough for primary `is_joint=True`;
- define drive/operator/run resampling blocks;
- document any inherited Drive-1 data provenance separately.

---

## C. Secondary measured arms

### TU Wien SA-5G
DOI: `10.48436/hja53-s8y18`
- data: CC BY 4.0
- code: MIT
- 7 fixed indoor locations
- latency: 210 runs across target rates/locations/repetitions
- throughput: 35 runs
- 60 s runs, 1 s reporting
- latency and throughput campaigns are separate → `is_joint=False` unless a justified pairing rule is introduced and labeled as synthetic pairing.

### NYU-METS
Repository: `NYU-METS/Main`
- ODbL 1.0 database; DbCL 1.0 contents
- LTE mobility (bus/subway/ferry/car/rail)
- TCP throughput every 1 s
- RTT not verified in project audit → throughput-only backup.

---

## Admission decision at source-audit stage

- **SIGMETRICS 2026:** PASS T1/T2 source-level; proceed to row-level ingestion audit.
- **PAM 2025:** PASS T1/T2 source-level; proceed to row-level ingestion audit.
- **TU Wien SA-5G:** PASS license/provenance; secondary arm only because joint throughput/latency is not established.
- **NYU-METS:** PASS license/provenance for throughput-only sensitivity; not sufficient alone for the primary measured q replay.

No confirmatory R2/R3 analysis is authorized by this source-level audit.
