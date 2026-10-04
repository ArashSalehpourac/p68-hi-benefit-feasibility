# P68-R4A v2 — Glasgow 5G outcome-blind preflight result

Date: 2026-10-04  
Status: **PASS — INDEPENDENT STATIONARY-5G FAMILY ADMITTED FOR R4B**

## Source integrity

- Dataset: Glasgow 5G Dataset 2025, Zenodo v2.
- DOI: `10.5281/zenodo.20465872`.
- License: CC BY 4.0.
- XLSX MD5: `375c58bd79d1e0762724fb78f67b4230`.
- XLSX SHA-256: `e293c28088305e1df331edfbdd49c12ab3a0415291e1be82cebbb9a8df7af4dd`.

The repaired parser removed only the 14 fully blank separator rows per daily sheet. Canonicalization yielded exactly:
- 720 sessions;
- 3 dates;
- 15 locations;
- 4 providers;
- 2 devices;
- 24 frozen temporal blocks = date × provider × device;
- 30 sessions/block.

Upload throughput and ping RTT are jointly present in each released session row.

No P2 inference benefit, correctness, confidence or policy outcome was loaded.

## Frozen E2E gate result

Pair-specific admissible windows:
- Pair A: **30–45 ms**;
- Pair B: **25–40 ms**.

Global common admissible window:
- **30–40 ms**.

Outcome-blind primary Glasgow deadline:
- **35 ms**.

At 35 ms, both empirical-service constructions remain comfortably non-saturated.

Pair A block feasibility:
- p10 ≈ 0.326;
- p50 ≈ 0.373;
- p90 ≈ 0.491;
- no blocks <0.05 or >0.95.

Pair B:
- p10 ≈ 0.486–0.487;
- p50 ≈ 0.624–0.625;
- p90 ≈ 0.684;
- no blocks <0.05 or >0.95.

Provider-level feasibility is also non-saturated.

## Decision

Glasgow 5G passes R4A trace admission and provides an informative independent stationary public-5G regime.

This family is scientifically distinct from the PAM mobility trace. It supports an **independent stationary urban 5G replication**, not a second mobility replication.

Before any P2 benefit/policy outcome is reused on Glasgow, R4B must freeze and audit a causal Glasgow feasibility estimator at the shared 30–40-ms support window.
