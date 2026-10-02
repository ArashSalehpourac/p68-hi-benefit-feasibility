# P68 — Benefit–Feasibility Coupling in Hierarchical Edge Inference

Working title: "When Hard Inputs Are Also Hard to Deliver: Benefit–Feasibility Coupling and Class-Tail Failure in Deadline-Constrained Hierarchical Inference"

Created: 2026-10-01. Owner: Arash Salehpour. README v2 (adds GitHub URL; v1 kept as 00_README_P68_v1_superseded.md).

## Workspaces
- Drive folder: https://drive.google.com/drive/folders/1UPMHOYOQlqz49h_ITDGEXOBIw5Tv_8_A (id 1UPMHOYOQlqz49h_ITDGEXOBIw5Tv_8_A)
- Slack: #p68-hi-benefit-feasibility (channel id C0C5TD4GFBM)
- ClickUp: folder "P68 — Benefit–Feasibility Coupling in Hierarchical Edge Inference" (folder id 1100340000086813), lists 00-06
- GitHub: https://github.com/ArashSalehpourac/p68-hi-benefit-feasibility (created by the researcher; files not yet committed as of this README)

## Status (2026-10-01)
Proposal v4-final: pilot protocol FROZEN; full ImageNet-scale study blocked until pilot gates G1, G3, G4 pass on real ImageNet-scale payloads.

Integrity hashes (SHA-256 of the local files when frozen; Drive copies have identical byte sizes):
- proposal_v4_final.md (13,109 bytes): 3d40c2d32394127cc99f8244490a83a9fd266806edd5891f7bf28d3854f89b73
- proposal_v4_review_prompt.md (14,251 bytes): f40c9b291f64872c3ccfbdb717cd75176d9cd8a37c14dfd7218a901b0a4a3d8e
Verify after download with `sha256sum`.

## Files in this folder
| File | What it is |
|---|---|
| 00_README_P68.md | this index |
| proposal_v4_final.md | frozen pilot protocol, estimand, gates, change log |
| proposal_v4_review_prompt.md | the prompt sent to external reviewers (superseded by v4-final) |
| reviews_v4_round_R1_R2_R3_verbatim.md | three external reviews of v4 (verbatim, links stripped) |
| REVIEW_LOG.md | all review rounds, decisions, rejected suggestions |
| pilot_payload_vs_severity.py | P0 payload-vs-severity script (docstring corrected: ILSVRC val images are already JPEG) |
| censor_sim.py | synthetic screen showing no censoring bias when stationary |

## Open items
1. Trace licensing (Ghoshal 2022, Khan 2025): none found; request author permission or use fitted distributions only.
2. ImageNet validation images needed for P0/P2 (CIFAR-10-C is plumbing only).
3. Researcher to confirm SESOI (>=2 pp AND >=20% of recoverable class-tail benefit), G3 threshold (0.10), G10 margins.
4. Commit the frozen files to GitHub; release scripts, hashes and metadata only (no ImageNet-derived images, no raw traces).
5. Reviewer-supplied citations not verified by Claude: Jellyfish, DACC, AutoJPEG, Moothedath et al., Beytur et al., Pacheco et al., EdgeBoost, Hu et al., H2T2, Neurosurgeon, Edge AI (Li et al.), SPINN, LimitNet, CICO.

## Not saved here
The first two review panels of the v3 round were not available to Claude as text after the session was compacted; only their verdicts are recorded in REVIEW_LOG.md. The third and fourth v3-round reviews are summarized there as well. Original uploaded files remain in the chat session.
