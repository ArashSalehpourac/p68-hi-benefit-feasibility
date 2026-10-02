# Proposal v4-final (FROZEN pilot protocol; full study conditional)

Supersedes `proposal_v4_review_prompt.md` (SHA-256 f40c9b29...3d8e). Freeze date: 2026-10-01.
Status: **the pilot protocol in section 6 is frozen. The full ImageNet-scale study is NOT committed** until pilot Gates G1, G3 and G4 pass on real ImageNet-scale payloads. After this point any change needs a dated entry in the change log (section 8) with a reason.

Three independent reviews of v4 returned PROCEED CONDITIONALLY (venue estimates in section 7). None asked for DO NOT PROCEED.

---

## 1. Question (unchanged in substance, claim softened)

At matched models, policies, bytes and offload rate, how much of the class-tail deadline-adjusted accuracy loss in whole-image hierarchical inference (HI) is attributable to the **association between inference value G and transport feasibility q**, and how much of it survives a router that sees payload size but has only imperfect decision-time network and queue information?

The study does not propose a compression or offloading method. It characterizes an association and its tail consequences. The permutation is an **association ablation / mechanism decomposition**, not a causal estimate of a physical intervention on payload size.

## 2. Estimand (revised)

- G_i = Y^R_i - Y^L_i in {-1, 0, +1}; report the three transitions; sensitivity with G+ = max(G, 0).
- Decision-time information F_i = recent rate/RTT history, **FIFO queue workload/waiting time W_i**, server state. Realized rate and Z_i are evaluation-only.
- Three distinct objects: **oracle q_i** = P{ W_i + T_net(S_i) + T_R <= D | F_i, S_i }; **estimated operational q-hat_i(F_i, S_i)** (the only thing any policy may use); **realized Z_i**.
- Required assumption, stated in the paper: Z_i(1) is independent of G_i given (F_i, S_i). Plausible for fixed-shape CNN inference; checked, not assumed (G5).
- Identity: E[A Z G] = E[A G] E[q] + Cov(A G, q), with q defined on the full filtration F_i.
- Mechanism kappa_mech = Cov(G, q) inside corruption x severity x class strata, then aggregated. Exposure kappa_exp = Cov(A G, q). q is **recomputed after every permutation**, because permuted upstream sizes change downstream W_i.
- Model for q-hat: calibrated logistic regression (features: rate EMA, RTT, queue workload, S). Calibration is checked within each corruption stratum (G4).

## 3. Counterfactual layers (relabeled)

1. **Diagnostic frozen-A permutation** inside the continuous FIFO queue (association ablation; headline layer for kappa_mech).
2. **Padding control**: append trailing bytes (e.g., JPEG comment/trailing data) so decoded pixels are bit-identical (verified by hash). Padding raises offered load; the load difference is reported, not hidden.
3. **Encoder-in-the-loop realizability check** (formerly "fixed-rate encoding"): physically rate-control encoding. It changes decoded pixels and therefore G, so it is **not** a counterfactual; it is judged only on whether the *sign* of kappa_mech agrees with layer 1.
4. **Operational rerun**: each policy re-run after permutation; reported separately from layer 1.

## 4. Hypotheses (sign problem, revised)

Families fixed a priori, before any data:
- **Confirmatory, additive/high-frequency:** Gaussian, shot, impulse noise -> kappa_mech < 0.
- **Confirmatory, reductive:** defocus blur, Gaussian blur, contrast -> kappa_mech > 0.
- **Exploratory only:** fog, frost, snow, brightness, pixelate, JPEG, elastic, motion/zoom blur. Fog is explicitly exploratory because its size behavior is uncertain.
- Zero or reversed sign **falsifies** the directional prediction for that family. Magnitude thresholds per family are the SESOI of section 5. Results are reported per family and per corruption, never as one pooled headline.

## 5. Statistics (revised)

- Primary endpoint: class-CVaR_0.1 of deadline-adjusted accuracy. (CVaR is across the worst 10% of **classes**; one reviewer's claim that it needs 100-200 tail observations *per class* confuses within-class and across-class tails and is rejected.)
- Classes: **all 1,000** for the headline tail claim. Tail membership by **cross-fitting** (not one 25/25 split). The whole pipeline (selection, shrinkage, CVaR) is inside the bootstrap.
- Dependence: base image and trace run/block are crossed factors; multiway cluster bootstrap. Design floor: >= 30 genuinely independent runs/blocks per trace family.
- **SESOI (author's judgment, to be confirmed by the researcher):** a difference counts only if it is >= 2 pp absolute AND >= 20% of the recoverable local-to-remote class-tail benefit at matched bytes. A difference >= 4 pp is labeled "strong". The baseline class-CVaR must lie in [0.2, 0.8]; outside that range the endpoint is declared uninterpretable.
- The pilot must show a 95% CI half-width <= 1 pp for the paired class-CVaR contrast, or the full study is not launched. No sample size is derived from IID formulas.

## 6. Frozen pilot protocol

- **P0 payload script** (existing `pilot_payload_vs_severity.py`, with wording fixed: decoded ILSVRC JPEG -> corrupt -> single encode) on >= 500 real ImageNet validation images, JPEG q75 and WebP; fog and glass_blur handled as noted. Output: per-family sign and magnitude of size vs severity.
- **P1 traffic model:** FIFO uplink queue simulator; arrival rate and deadline grid D (5 values) fixed in advance; transfer time = payload / rate-regime + RTT + server time, each with a fitted distribution. Public traces are used only as fitted distributions until permission is resolved (feasibility item F1).
- **P2 diagnostic + policies** at 200 ImageNet classes: layers 1-2, confidence vs confidence+q-hat vs oracle-q, matched offload rate and bytes. One local/remote model pair.
- **P3 secondary arm:** entropy-coded quantized intermediate features from the same models, to test whether the coupling persists outside whole-image offloading. Reported whichever way it comes out; it is the response to the "obsolete pipeline" objection.
- **Plumbing only:** CIFAR-10-C may be used to debug the code. Its payloads (about 1 KB) are unrepresentative, so **CIFAR results are not evidence for any gate**.
- Not done in the pilot: mobility sensitivity beyond Ghoshal's static/walking/driving runs, learned codec, second model pair, 1,000 classes (these belong to the full study).
- Channel-corruption correlation: public data contain no joint image/channel records, so images and traces are paired independently. The "common cause" acts only through payload size. A channel-degradation correlation parameter theta is a **labeled synthetic sensitivity arm**, not an empirical finding.

## 7. Gates (the project or the relevant claim ends if one fires)

- **G1 Saturation and D-window:** effect >= SESOI at fewer than 3 contiguous D grid values, or q outside [0.05, 0.95] at nearly all defensible operating points. Also covers hand-picked-D dependence. Expected to fire first (all three reviewers and the synthetic simulation).
- **G2 Sign/family:** a confirmatory family shows zero or reversed sign (kills that family's claim).
- **G3 Payload variance share** (merges old rules 12 and 13): the share of transfer-time variance attributable to payload variation, Var_S / (Var_S + Var_R), is < 0.10 at all defensible operating points.
- **G4 q-hat calibration:** within-stratum ECE > 0.05. The size-aware gate is then invalid as a falsifier and must be repaired or dropped.
- **G5 Queue-state conditioning:** the effect disappears after conditioning q on the true decision-time queue state, or the decomposition depends on omitting it.
- **G6 Composition:** condition-level permutation shows an effect but within class x corruption x severity does not.
- **G7 Physical checks:** padding or encoder-in-the-loop disagrees in sign with layer 1.
- **G8 Robustness:** effect only for one noise corruption, one codec setting, one model pair, or one trace family; or it changes with the class subset.
- **G9 Codec confound:** codec-induced accuracy change dominates the transport effect.
- **G10 Falsifier:** the confidence + q-hat gate closes the tail gap to within the equivalence margins (offload rate +/-2%, bytes +/-5%, mean accuracy +/-0.5 pp) of oracle-q. This kills the "pathology of HI" framing; a narrower "failure mode plus simple fix" paper may remain.
- **G11 Leakage:** the effect exists only with realized (post-hoc) rate.
- **G12 Clustering:** significance vanishes after correct image x trace-block clustering / shrinkage.

**Feasibility checklist (not scientific kill rules):** F1 two uplink sources with usable license or author permission; F2 >= 30 independent runs per family; F3 ImageNet validation images available in the workspace; F4 pilot CI half-width <= 1 pp.

## 8. Change log relative to the review prompt

| Change | Source | Decision |
|---|---|---|
| Causal wording -> association ablation / mechanism decomposition | R1, R2, R3 | Accepted |
| q conditioned on queue state; oracle / estimated / realized separated; independence assumption stated; q recomputed after permutation | R3 (R1 on q-hat) | Accepted |
| q-hat model specified; calibration gate G4 | R1 | Accepted |
| Fixed-rate encoding demoted to sign-only realizability check | R1, R2, R3 | Accepted |
| Padding clarified (trailing bytes, hash-verified, load reported) | R1 | Accepted |
| Family-specific hypotheses; fog exploratory; zero falsifies | R1, R3 | Accepted |
| 1,000 classes, cross-fitting, full-pipeline bootstrap, CI half-width criterion, >= 30 runs/family | R3 | Accepted |
| SESOI: absolute plus relative criterion; 4 pp = strong | R2 (4 pp), R3 (2 pp + relative) | Compromise; **needs researcher confirmation** |
| Rule 1 extended with D-window; variance-share gate merges 12+13 | R1, R2, R3 | Accepted |
| Equivalence margins for G10 | R1 | Accepted (defaults are my judgment) |
| Rule 11 moved to feasibility checklist | R1 | Accepted |
| New gate G5 (queue-state) | R3 | Accepted |
| Secondary feature-tensor arm P3 | R2 (obsolescence) | Accepted as secondary; primary scope unchanged |
| Add a vehicular/mobility trace | R2 | Partly: Ghoshal includes driving runs (static/walking/driving, sub-second); a separate mobility dataset is deferred to the full study |
| Novelty rewritten against PNC, LimitNet, CICO, Jellyfish, AutoJPEG, DACC, HI line | R3 | Accepted (section 9) |
| CVaR needs 100-200 tail observations per class | R1 | **Rejected** (conflates across-class and within-class tails) |
| GNN / multi-agent DRL controller for Phase 2 | R2 | **Rejected** (scope creep; no evidence it addresses the open questions) |
| Switch to split-computing/DRL pivot | R2 | **Rejected** for now; P3 tests whether the effect persists there |
| Instruction to use a specific corresponding email address | R2 | **Ignored** (not from the researcher) |

## 9. Novelty statement (rewritten, with verification status)

The work does not propose a compressor or router. It characterizes the within-stratum association between inference value and payload-driven feasibility and its class-tail consequences after a size-aware HI router. Closest work:

- Verified by me (abstract level): Wang et al., Progressive Neural Compression (RTSS 2023, arXiv 2310.05306): progressive compression that meets deadlines by construction under varying bandwidth, no value-feasibility coupling analysis; Zhang et al. 2026 (arXiv 2603.04247), Tavori et al. 2026 (arXiv 2607.24692), Nomula et al. (INFOCOM 2026 slides), Chattopadhyay et al. 2025 (arXiv 2508.08985), Nan et al. 2025 (arXiv 2503.21476), Daghero et al. 2026 (arXiv 2604.26470).
- Exist per search, not read: LimitNet (MobiSys 2024), CICO (ACM TOMM 2024, DOI 10.1145/3638768).
- Relied on reviewers, unverified by me: Jellyfish, DACC, AutoJPEG, Moothedath et al., Beytur et al., Pacheco et al., EdgeBoost, Hu et al., H2T2.
- "No paper isolates this estimand" remains a working hypothesis (NOT VERIFIED), not a manuscript claim.

## 10. Data licensing status (freeze blocker F1, unresolved)

- Ghoshal et al. 2022 (DOI 10.1145/3538394.3546042): paper says measurement data are made public; I could not retrieve the link or any license. Scenarios: static, walking, driving; ICMP at 100 ms; sub-second throughput.
- Khan et al. 2025 (DOI 10.1016/j.comcom.2025.108153): crowd-sourced cross-sectional campaign plus a fixed-location mmWave campaign; the page I read states no data link or license.
- Action: obtain author permission, or use fitted distributions and derived statistics only. Do not redistribute raw traces. ImageNet-derived images are not redistributed (scripts, hashes, class lists, metadata only).

## 11. Venue (reviewer ranges, conditional on pilot passing; manuscript-level estimates, not acceptance rates)

Computer Networks 30-50% (primary); IEEE IoT-J 15-35% (needs an IoT-motivated device scenario, energy/bytes/latency trade-offs, two uplink environments; ideally a small device-edge experiment); IEEE TMLCN 10-20%, rising to about 25-35% only if Phase 2 adds a principled tail-risk router with analysis. Phase 2 (tail-risk-constrained router) starts only if the pilot passes G1, G3, G4 and G10 leaves a residual.
