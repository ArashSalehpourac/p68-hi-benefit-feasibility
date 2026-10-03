# P68-R1M v2 — Balanced remote-service stability review

Date: 2026-10-03
Status: **FAIL STABILITY GATE — REMOTE SERVICE NOT FROZEN**

## Reproducibility audit

The exact-reproduction correction worked:
- primary non-impulse corpus: 336/336 JPEG q75 byte counts exactly reproduce frozen P2;
- impulse-noise sensitivity: 0/80 exact, retained only as sensitivity;
- no inference benefit/correctness/confidence/policy outcome was loaded.

## Hardware / software

- GPU: Tesla T4, compute capability 7.5;
- PyTorch 2.11.0+cu130;
- torchvision 0.26.0+cu130;
- CUDA 13.0;
- cuDNN 92700;
- scikit-image 0.25.2.

## Primary exact-reproduction pooled service timing

- ConvNeXt-Base + JPEG: p95 22.430 ms, bootstrap CI 21.849–23.048;
- ConvNeXt-Base + WebP: p95 23.715 ms, bootstrap CI 23.280–24.444;
- ViT-B/16 + JPEG: p95 12.719 ms, bootstrap CI 12.511–13.124;
- ViT-B/16 + WebP: p95 14.372 ms, bootstrap CI 13.978–14.768.

## Frozen stability gate

ConvNeXt arms pass:
- JPEG round-p95 CV 0.0454, max/min 1.1196, CI relative width 0.0534;
- WebP round-p95 CV 0.0271, max/min 1.0640, CI relative width 0.0491.

ViT arms fail:
- JPEG round-p95 CV 0.1053 (>0.10), max/min 1.3195 (>1.20);
- WebP round-p95 CV 0.1043 (>0.10), max/min 1.2984 (>1.20).

Therefore the pre-specified all-arm stability gate fails. No hardware-specific E2E deadline grid is frozen.

## Thermal-state diagnosis

Telemetry shows sustained heating during the run. ConvNeXt begins near 52 C and ends near 73 C. ViT then begins near 72–73 C and reaches about 80–81 C, with graphics clocks falling as low as ~1425 MHz by the last ViT round.

ViT round 0 is systematically faster than later rounds (JPEG p95 10.265 ms vs 12.666–13.544 ms; WebP 11.402 ms vs 14.071–14.805 ms). The randomized content order rules out the previous content-order confound. The remaining instability is consistent with hardware thermal/power-state drift and must be controlled before freezing a service component.

## Decision

- Do not loosen the existing stability thresholds.
- Do not drop the failing ViT round post hoc.
- Run R1N with a fixed, outcome-blind model-specific thermal preconditioning period, then repeat the same randomized balanced corpus and the same R1M stability gate.
- If R1N passes, freeze pooled p95 under the explicitly labeled sustained-warm Tesla T4 condition.
- If R1N fails, stop trying to estimate a single service constant and carry service latency as an empirical distribution / sensitivity rather than a fixed p95 component.