# P68-R4A v2 — Glasgow parser repair

Date: 2026-10-04
Status: **FROZEN BEFORE ANY R4A E2E OUTCOME**

R4A v1 stopped at the per-sheet row-count assertion before canonicalization or E2E feasibility analysis.

Direct workbook inspection shows each daily raw sheet contains 254 rows after the header: **240 nonblank measurements plus 14 completely blank separator rows** between location sections. The 240 measurements/day exactly preserve the frozen design: 15 locations × 4 providers × 2 devices × 2 sessions.

R4A v2 changes ingestion only: record raw rows, assert 14 rows are completely empty, drop only rows with all columns missing, reset index, then assert 240 measurement rows remain. No partially populated row may be removed.

All source hashes, schema fields, block definition, service construction, deadline grid, non-saturation gate, and interpretation rules remain unchanged. Because v1 stopped before any E2E outcome, this repair is pre-outcome.