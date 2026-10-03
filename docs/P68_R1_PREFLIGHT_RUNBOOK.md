# P68-R1 network-only preflight runbook

Date: 2026-10-03  
Status: executable preflight only; no benefit/policy outcome analysis is authorized here.

## Why this is the next step

The post-rejection redesign requires measured-network evidence before any new policy claim. The first execution therefore audits the preferred SIGMETRICS'26 cellular traces without reading P2 benefit data.

## A. Pull only the Alaska SIGMETRICS'26 archive

Pinned upstream commit:

`b5f330d508e08e8e1fcd2300529a45f1bbb3231d`

Git-LFS object recorded by GitHub:

- SHA-256: `e3f16483793553dba15f6b735efeb9b18aba14589156c4637795317f00e2d311`
- size: `28,477,528` bytes

Suggested shell sequence:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/NUWiNS/sigmetrics26-exploring-the-5g-digital-divide-in-the-non-contiguous-us-leo-satellites-to-the-rescue.git
cd sigmetrics26-exploring-the-5g-digital-divide-in-the-non-contiguous-us-leo-satellites-to-the-rescue
git checkout b5f330d508e08e8e1fcd2300529a45f1bbb3231d
git lfs pull --include="datasets/alaska_road_test_202406.processed.tar.gz"
sha256sum datasets/alaska_road_test_202406.processed.tar.gz
stat -c '%s' datasets/alaska_road_test_202406.processed.tar.gz
mkdir -p /content/p68_sigmetrics26_alaska
tar -xzf datasets/alaska_road_test_202406.processed.tar.gz -C /content/p68_sigmetrics26_alaska
find /content/p68_sigmetrics26_alaska -type f -path '*/ping/*.csv' -print
```

The checksum and byte count must match before use.

## B. Preflight every cellular ping table

The upstream README documents Alaska/Hawaii `ping/<op>_ping.csv` tables as containing:
- `rtt_ms`
- `operator`
- concurrent smart-throughput DL and UL fields
- XCAL radio context.

For P68 whole-image offload, use **uplink** throughput by default.

From the P68 branch `post-rejection-redesign`:

```bash
python scripts/trace_ingest_preflight.py \
  --source sigmetrics26 \
  --input_csv <PING_CSV> \
  --direction uplink \
  --source_family sigmetrics26 \
  --source_commit b5f330d508e08e8e1fcd2300529a45f1bbb3231d \
  --campaign alaska_202406 \
  --out_prefix results/r1_preflight/sigmetrics26/<operator_or_run>
```

The script writes a canonical trace, JSON report and one-row CSV report. It computes the local input SHA-256 automatically and never reads P2 predictions/benefit.

## C. Admission checks

Do not proceed to routing outcomes until the trace-level report is reviewed for:
- timestamp order and duplicates;
- actual sample interval;
- long gaps;
- missing / zero throughput semantics;
- RTT missingness / zero values;
- run/operator/segment identifiers;
- evidence that the selected throughput and RTT fields are genuinely concurrent;
- no-service / padding semantics.

A `PASS` from the script means only that basic mechanical checks did not trigger. It is **not** scientific approval of the trace.

## D. PAM'25 replication smoke test

Pinned upstream commit:

`782b712599f3710f7d3acff57097af6ca14660ae`

Two recorded Git-LFS objects for an initial AT&T Drive-2 schema/alignment audit:

- RTT: `datasets/processed_files/extracted_ping_data/atnt/d2/rtt_atnt2.csv`
  - SHA-256 `a27a5494d31db05de3ee85a81561db9ace62cd57a09036c3486f7b3d44760853`
  - size `463,546` bytes
- DL throughput example: `datasets/processed_files/extracted_tput_data/atnt/DL/atnt_day_1_d2_dl.csv`
  - SHA-256 `ef53a5d555bed97339bc8f3fc2764a30b20858ededab9e0c2044a008cb9b9de7`
  - size `4,910,642` bytes

These are separate upstream files. **Do not set `is_joint=True`** until the exact timestamp overlap and alignment rule are audited. Because P68's transmission is uplink, the eventual PAM replay must use the UL counterpart; the DL object above is only a schema smoke-test example recorded during source inspection.

## E. Stop condition for this phase

If the SIGMETRICS ping tables do not provide a defensible joint uplink-throughput + RTT time series after row-level inspection, stop and repair the trace construction before running any P2-coupled or policy analysis.
