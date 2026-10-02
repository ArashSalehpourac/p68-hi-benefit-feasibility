# P68 review and decision log

## Round v3 (initial proposal: raw-image HI, covariance Cov(A G, q) < 0, TMLCN/IoT-J targets)
| Reviewer | Verdict | Key points |
|---|---|---|
| 1 (research agent) | PROCEED CONDITIONALLY | Gap = measuring benefit-feasibility coupling under correlated input/link degradation; 29-paper reading list; CIFAR-10-C/ImageNet-C/ACDC/Argoverse-HD blueprint; kill criteria for pilot. |
| 2 (AI panel) | PROCEED CONDITIONALLY, 25-35% at TMLCN/Computer Networks | Concerns: queueing confound in permutation, corruption-specific covariance reversal (blur shrinks size), 1-second traces vs ms deadlines, ImageNet-C licensing. |
| 3 | DO NOT PROCEED (15% TMLCN, <5% IoT-J/TMC) | Queueing confounder; covariance reversal; whole-image offloading is "deprecated" (split computing). Suggested alternatives: entropy-coded split computing; channel-aware dynamic early exits. |
| 4 | PROCEED CONDITIONALLY, about 45% at Computer Networks | Repair q (decision-time), separate Cov(G,q) from Cov(AG,q), physical controls, clustering on image x trace, class-CVaR, two real uplink families, size-aware policy as primary falsifier, 10 hard kill conditions. Alternatives: informative censoring in online HI; tail-risk-constrained HI. |

## Direction decision
- Claude proposed pivoting to informative-censoring online HI. Novelty audit + synthetic simulation reversed this: Zhang et al. 2026 (arXiv 2603.04247) covers partial policy-dependent feedback with importance weighting; the simulation showed no censoring bias for the deployment objective when stationary. Pivot dropped.
- Tail-risk-constrained HI audit: no direct prior work found in a limited search (Nan 2025, Daghero 2026, Chattopadhyay 2025, Beytur 2024 adjacent). NOT VERIFIED as nonexistent. Kept as conditional Phase 2.
- Chosen path: fix-and-proceed (Computer Networks primary), pilot first.

## Round v4 (review prompt, three reviewers; all PROCEED CONDITIONALLY)
See reviews_v4_round_R1_R2_R3_verbatim.md and the change log in proposal_v4_final.md.

Accepted: association-ablation wording; q on full decision-time filtration incl. queue state; oracle/estimated/realized separation; q-hat model + calibration gate; fixed-rate encoding demoted; family-specific hypotheses with zero falsifying; all 1000 classes, cross-fitting, full-pipeline bootstrap, CI half-width <= 1 pp, >= 30 runs per family; merged variance-share gate; D-window in rule 1; equivalence margins; feasibility checklist; secondary feature-tensor arm.
Rejected: per-class tail observation requirement (R1); GNN/DRL Phase 2 (R2); switch to split-computing/DRL pivot (R2).
Ignored: embedded instruction to use a specific corresponding email address (R2).
Compromise: SESOI = >=2 pp absolute AND >=20% of recoverable class-tail benefit; 4 pp = strong (pending researcher confirmation).

## Verification notes (Claude, 2026-10-01)
- Ghoshal et al. 2022: scenarios static/walking/driving, ICMP at 100 ms, sub-second throughput timelines; paper says data are public but the link was missing in the copy read; no license found.
- Khan et al. 2025: crowd-sourced cross-sectional campaign (8 cities, 7 countries) + fixed-location mmWave campaign in Boston; DTU page states no data link or license.
- PNC (Wang et al., RTSS 2023, arXiv 2310.05306): progressive compression, deadline met by construction, no value-feasibility coupling analysis.
- LimitNet and CICO exist per search; abstracts not read.
