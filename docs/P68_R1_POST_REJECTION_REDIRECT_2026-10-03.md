# P68-R1 — Post-rejection redesign protocol (DRAFT; NOT FROZEN)

Date: 2026-10-03
Parent evidence branch: `post-freeze-pilot-p1-p2` @ `f4cb9ed8148c8f5d04d6986d4466a7a1293459ed`
New working branch: `post-rejection-redesign`

## 0. Reason for redesign

Computer Networks rejected the submitted P68 manuscript in its current form, stating that it did not yet have the scientific significance / archival value required by the journal and that more work was needed to substantiate the conclusions.

This record does **not** reinterpret the frozen pilot. The original P2 directional mechanism remains falsified under the pre-specified G2 sign rule. The completed negative-result evidence and the rejected manuscript are historical inputs to a new study.

The new study asks whether the pilot's scale-separation result has an **operational systems consequence under measured network dynamics**.

## 1. New scientific question

Primary question:

> Under measured cellular-network dynamics, when is deadline-adjusted hierarchical-inference utility well approximated by a factorized decision rule that separately predicts inference benefit and transport feasibility, and when does a joint interaction model materially improve routing decisions?

Secondary questions:

1. Does the near-zero/reversed within-stratum benefit–feasibility coupling observed in the pilot persist under measured throughput/RTT traces?
2. Can pooled/regime-level association be large while request-level conditional dependence remains weak under real network dynamics?
3. Does ignoring benefit–feasibility interaction change deadline-adjusted accuracy, transmitted bytes, deadline misses, or class-tail performance?
4. Which conclusions survive changes in model pair, codec, and representation/offload point?

## 2. Evidentiary separation

- **Legacy frozen pilot:** unchanged; no new confirmatory claim is retroactively attached to it.
- **R1 feasibility/trace audit:** may begin immediately.
- **R2 measured-trace replay:** may begin after trace schemas and licenses are verified.
- **R3 policy benchmark:** confirmatory analysis requires a frozen SESOI and fixed model/policy definitions before outcome comparison.
- **R4 external-validity expansion:** conditional on R2/R3 showing that the question is informative rather than saturated.

## 3. Candidate measured trace families (audit before use)

### A. NUWiNS SIGMETRICS 2026 drive-test artifact — preferred primary candidate
Source:
https://github.com/NUWiNS/sigmetrics26-exploring-the-5g-digital-divide-in-the-non-contiguous-us-leo-satellites-to-the-rescue

Verified from the public artifact:
- real road tests in Alaska, Hawaii, and a mainland-US baseline;
- cellular operators include AT&T, Verizon, and T-Mobile depending on campaign;
- throughput and RTT measurements are released;
- ping files for Alaska/Hawaii include ICMP RTT and concurrent smart-throughput fields;
- dataset license: CC BY 4.0;
- software license: MIT.

Primary use if schema audit passes: timestamp-preserving throughput/RTT replay with route/operator blocks.

### B. NUWiNS PAM 2025 multi-carrier artifact — preferred independent replication candidate
Source:
https://github.com/NUWiNS/pam2025-multi-carrier-dataset

Verified from the public artifact:
- mobile measurements over three cross-US routes;
- AT&T, T-Mobile, and Verizon;
- throughput data plus ping/RTT data with timestamp-processing/alignment scripts;
- repository license: CC0-1.0.

Primary use if schema audit passes: independent mobility/operator replication.

### C. TU Wien private-SA-5G measurement dataset — secondary controlled measured-network arm
Source:
https://researchdata.tuwien.ac.at/records/hja53-s8y18
DOI: 10.48436/hja53-s8y18

Verified from the dataset record:
- measured end-to-end latency and TCP throughput in a private standalone 5G network;
- seven fixed indoor locations;
- 60-second runs with one-second reporting;
- data license: CC BY 4.0; code: MIT.

Use: controlled 5G external-validity sensitivity. Latency and throughput campaigns were measured separately, so this arm must not be represented as a joint mobile trace.

### D. NYU-METS — throughput-only mobility backup
Source:
https://github.com/NYU-METS/Main

Verified from the public artifact:
- LTE mobile bandwidth traces in bus/subway/ferry/car/rail scenarios;
- TCP throughput sampled every 1 s;
- database license: ODbL 1.0; contents: DbCL 1.0.

Use only as a throughput-only sensitivity unless a matching measured RTT source is separately justified.

## 4. R1 trace-admissibility gates

A trace family is admitted only if all applicable items are documented before the primary replay:

- **T1 License:** explicit redistributable/research-use license verified.
- **T2 Provenance:** collection campaign, operator/network type, timestamps, and units documented.
- **T3 Temporal fidelity:** primary replay preserves original time order; no IID reshuffling of rate/RTT samples.
- **T4 Block definition:** route/day/run/operator blocks are fixed before policy comparison and are the resampling unit for network uncertainty.
- **T5 Jointness:** if throughput and RTT were not measured jointly, the arm is labeled accordingly and cannot support claims about their empirical cross-correlation.
- **T6 Window:** deadline grid is defined from network-only quantities before benefit/policy outcomes are examined.
- **T7 Saturation:** regimes with effectively all-success or all-failure deadlines are reported but do not drive the primary interaction comparison.

## 5. R2 measured-trace replay

Reuse the current P2 image/benefit/payload evidence where possible. Regenerate inference outputs only for fields that are absent (e.g., local confidence/logits or additional codecs).

For each admitted trace block:

1. replay requests in trace time order;
2. maintain FIFO queue state;
3. compute actual transfer time from payload bytes and measured time-varying link information using a pre-specified interpolation/holding rule;
4. use measured RTT when jointly available;
5. include remote compute time as a separately identified component;
6. record realized deadline success Z and decision-time feasibility estimate q-hat;
7. do not let policies access post-decision measurements.

Primary diagnostic:
- request-level conditional association between realized benefit G and feasibility q / realized deadline success, with image and trace-block uncertainty propagated.

Sensitivity:
- Pearson residualized association;
- Spearman residualized/rank association;
- pre-specified nonlinear interaction test/model comparison;
- pooled versus matched/conditional decomposition.

The pilot's Pearson statistic remains historical; R2 does not overwrite it.

## 6. R3 operational policy benchmark

Policies are compared at matched operating budgets.

Baselines:
- Local only.
- Confidence-only offloading.
- Network/payload-aware gate added to confidence.
- **Factorized utility policy:** separately estimate expected remote benefit and deadline feasibility, then combine them at decision time.
- **Joint interaction policy:** one model directly predicts deadline-adjusted remote utility from image-side and network-side observable features.
- Oracle-q diagnostic.
- Oracle realized-benefit ceiling (diagnostic only; never described as deployable).

Matching:
- primary comparison at matched offload rate;
- secondary comparison at matched transmitted-byte budget;
- report remote-compute invocation count separately.

Primary endpoint:
- deadline-adjusted top-1 accuracy.

Secondary endpoints:
- deadline-miss rate;
- transmitted bytes;
- mean top-1 accuracy without deadline adjustment;
- class-tail/CVaR endpoint only after its definition and SESOI are frozen;
- per-trace-family and per-model-pair effects.

Key estimand:
- paired performance difference between the factorized and joint policies under the same image/trace blocks and matched budget.

## 7. R3 statistical design

- Images and network trace blocks are separate dependence sources.
- Use a crossed / multiway resampling scheme that resamples images and trace blocks at their natural units.
- Report per-trace-family results before any cross-family summary.
- No IID request-level confidence interval is acceptable as headline evidence.
- Hyperparameter selection and policy calibration must be separated from the held-out trace blocks used for final evaluation.
- Any threshold search that uses deadline-adjusted accuracy must be nested inside training/validation resampling.

### SESOI — OPEN, blocks confirmatory freeze

The prior proposal used a candidate threshold of >=2 percentage points absolute and >=20% of recoverable class-tail benefit, with >=4 pp called strong. The author never explicitly confirmed that judgment in the project record.

Therefore **no confirmatory R3 gate is frozen yet**. R1 trace audit and implementation can proceed, but the R3 confirmatory comparison must not be run until the SESOI and any equivalence margin are dated and frozen.

## 8. R4 external-validity expansion (conditional)

If R2/R3 are informative:

- expand from 200 to all 1,000 ImageNet classes for the headline class-tail claim;
- add at least one additional local→remote architecture pair beyond the two pilot pairs;
- JPEG and WebP at more than one quality/rate point;
- add one split/feature-tensor representation arm;
- repeat on both preferred measured cellular trace families;
- keep natural/deployment-like shift separate from synthetic ImageNet-C corruption.

If R2/R3 show no actionable interaction and factorized/joint policies are equivalent within the frozen margin, stop rather than adding scale solely to chase significance.

## 9. Kill / redesign rules

- **K1 Trace insufficiency:** no two admissible measured trace families with documented licenses and usable temporal information → do not make a broad real-network claim.
- **K2 Saturation:** the chosen deadline region is uninformative across most measured blocks → redesign the network-only deadline grid before policy outcomes.
- **K3 No operational consequence:** factorized and joint policies are equivalent within the frozen margin across measured trace families → paper, if written, must frame the result as a validated simplification/boundary result, not an interaction pathology.
- **K4 One-family dependence:** a material effect appears in only one trace family/operator/route → no general cellular claim.
- **K5 Leakage:** an effect requires realized post-decision rate/RTT or realized benefit → operational claim fails.
- **K6 Model/codec fragility:** an effect disappears under the planned external-validity arms → narrow the claim.
- **K7 Statistical fragility:** headline effect disappears under trace-block + image resampling or held-out-block evaluation → no confirmatory claim.

## 10. Immediate execution order

1. Freeze this document only after author confirms SESOI/equivalence margin; until then status remains DRAFT.
2. Audit and ingest candidate A (SIGMETRICS 2026) and candidate B (PAM 2025).
3. Write a trace-schema manifest: files, columns, timestamp units, throughput direction, RTT alignment, route/operator/run IDs, licenses.
4. Implement a measured-trace replay adapter with deterministic tests.
5. Run a **network-only preflight** (no G, no policy outcome): queue stability, deadline-window coverage, missingness, time alignment.
6. Freeze R2/R3 operational details.
7. Run measured-trace coupling diagnostics and the factorized-vs-joint policy benchmark.
8. Only then decide whether the 1,000-class / codec / split-representation expansion is warranted.

## 11. Current project state

- Frozen pilot: preserved.
- P2 G2 mechanism: failed; not reopened.
- Direct simulator G–q check: near zero; simulator-only.
- Computer Networks v1 manuscript: submitted and rejected for insufficient scientific significance / archival value.
- Appeal: not part of the current plan.
- Next scientific gate: **licensed measured-network trace audit + replay preflight**, not manuscript rewriting.
