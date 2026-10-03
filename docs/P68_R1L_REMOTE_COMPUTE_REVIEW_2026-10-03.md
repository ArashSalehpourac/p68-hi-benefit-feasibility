# P68-R1L — Remote-compute latency audit review

Date: 2026-10-03
Status: **PROVISIONAL — DO NOT FREEZE SERVICE p95 YET**

## What R1L established

R1L executed successfully on a **Tesla T4** (15,360 MiB; compute capability 7.5), PyTorch 2.11.0+cu130 / torchvision 0.26.0+cu130, CUDA 13.0, cuDNN 92700.

Batch-1 FP16-autocast warm service timing was measured for:
- ConvNeXt-Base (IMAGENET1K_V1);
- ViT-B/16 (IMAGENET1K_V1);
- JPEG q75 and WebP q75.

Provisional full-service p95 values:
- ConvNeXt-Base + JPEG: 23.458 ms (bootstrap 95% CI 22.817–24.038);
- ConvNeXt-Base + WebP: 23.465 ms (21.902–24.443);
- ViT-B/16 + JPEG: 13.464 ms (13.010–13.729);
- ViT-B/16 + WebP: 12.032 ms (11.338–12.616).

These are hardware-specific measurements, not universal server latency.

## Why the values are not frozen yet

### 1. The first-half/second-half timing diagnostic is confounded by input order

R1L reported p50 shifts of:
- ConvNeXt/JPEG: 16.4%;
- ViT/JPEG: 27.4%;
- ConvNeXt/WebP: 2.4%;
- ViT/WebP: 3.3%.

However, the service loop traverses an ordered content buffer and wraps after 416 inputs. The first and second halves therefore do not contain exactly balanced content/codec workloads. The diagnostic cannot distinguish temporal drift from content/order effects.

A randomized, balanced repeated-round timing audit is required before treating p95 as stable.

### 2. R1L did not reproduce P2's deterministic corruption seeding

The frozen P2 generator seeds each corrupted image as:

`np.random.seed(SEED * 1_000_003 + image_idx * 101 + condition_index)`

with P2 `SEED=0`.

R1L defined a new seed variable but did not apply this per-image/per-condition seed before calling `imagecorruptions.corrupt`. This does not invalidate the rough latency scale, but it means the benchmark input corpus is not bitwise tied to the frozen P2 corruption realization.

## Decision

- Keep the R1L latency numbers as **provisional hardware-scale evidence**.
- Do not yet freeze the p95 remote-compute component or derived E2E deadline grids.
- Run R1M:
  - exact P2 corruption seed semantics;
  - verify JPEG byte sizes against frozen `p2_inputs.csv`;
  - paired JPEG/WebP content;
  - randomized codec order;
  - repeated balanced rounds;
  - GPU telemetry by round;
  - pre-specified p95 stability gate.

No inference outcome is required for R1M.