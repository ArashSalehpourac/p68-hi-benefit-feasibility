# P68-R1I — T6 measured-network deadline-window preflight

Date: 2026-10-03  
Status: **PASS — network-component window admitted; end-to-end deadline not yet frozen**

## Frozen inputs

- PAM'25 canonical joint UL+RTT trace: 6,184 rows, 344 frozen 2-s blocks, 6 operator×drive strata.
- Canonical trace SHA-256: `270194e69c6b68b487d4529a9cf648a66a347e62393964c9119ff971b1658194`.
- P0 payload CSV SHA-256: `fe9ac5b6e75e5bcfe4f2cddf8905809205c003a3bec5f2ec0febd0cb3816c703`.
- P0 primary subset: 31,200 rows = 600 images × 26 conditions × 2 codecs (JPEG q75, WebP q75).
- No benefit, correctness, confidence, label, or policy outcome was loaded.

## Replay semantics

Measured application throughput is not treated as spare capacity. No synthetic FIFO queue is used.

For payload B bytes, measured UL throughput u Mbps and RTT r ms:

`serialization_ms = 8 B / (1000 u)`

Primary network-component proxy:

`L_net = serialization_ms + r`

For `u <= 0`, latency is infinite. Server/remote-compute latency is not included in T6.

## Pre-specified saturation gate

A codec passes when there are at least 3 consecutive 10-ms grid points where pooled feasibility lies in [0.20, 0.80] simultaneously under:
1. empirical row weighting;
2. equal weighting of frozen 2-s blocks;
3. equal weighting of the six operator×drive strata.

## Result

**T6 PASS for both codecs.**

- JPEG: 6 consecutive qualifying grid points, 60–110 ms.
- WebP: 6 consecutive qualifying grid points, 60–110 ms.
- At 70 ms:
  - JPEG row/block/stratum weighted feasibility = 0.5056 / 0.4728 / 0.4878.
  - WebP row/block/stratum weighted feasibility = 0.5279 / 0.4966 / 0.5091.

The measured trace therefore contains a non-saturated network-component operating window. The final end-to-end deadline remains open because remote-compute latency has not yet been frozen.

## Diagnostics at 70 ms

JPEG:
- condition feasibility range 0.3649–0.6853;
- operator×drive range 0.2659–0.5723.

WebP:
- condition feasibility range 0.3620–0.7423;
- operator×drive range 0.2884–0.5981.

Family-level row-weighted feasibility at 70 ms:
- JPEG: additive 0.4167, clean 0.5509, reductive 0.6345.
- WebP: additive 0.4140, clean 0.5912, reductive 0.6924.

These are network/payload diagnostics only and do not reopen the frozen P2 benefit mechanism.

## Decision

- T6 window gate: **closed PASS**.
- Freeze the network-component admissible region as **60–110 ms** for the next outcome-blind design stage.
- Do not treat this as the final end-to-end deadline grid.
- Next: freeze causal observability for online network features and the separately identified remote-compute component before any R2/R3 benefit or policy evaluation.
