# P68 — P0 payload pilot: RESULTS (final, 600 images)

Date: 2026-10-02 · Protocol: proposal_v4_final.md (SHA-256 3d40c2d3…f89b73; frozen 2026-10-01, unchanged)
Notebook: P68_P0_payload_pilot.ipynb · Source: ImageNet-1k validation (HF ILSVRC/imagenet-1k, streamed, shuffled, seed 0)
Settings: 600 images, 224x224, JPEG/WebP q75, 14 ImageNet-C corruptions x 5 severities (glass_blur skipped), 0 ERR rows.
image_ids sha256: recorded in run_meta_p0.json (image_ids_sha256).

## Verdict
Necessary precondition SUPPORTED: payload size moves in the pre-registered direction in 10/10 confirmatory codec x corruption rows.
This is NOT evidence about benefit G, queueing, or any gate G1-G12.

## Confirmatory rows (severity-5 median per-image size ratio vs clean; Spearman rho severity vs size)
| family | corruption | JPEG ratio (rho) | WebP ratio (rho) | matches |
|---|---|---|---|---|
| additive | gaussian_noise | 3.16 (0.66) | 4.61 (0.44) | yes |
| additive | shot_noise | 3.11 (0.65) | 4.54 (0.45) | yes |
| additive | impulse_noise | 3.14 (0.58) | 4.57 (0.43) | yes |
| reductive | contrast | 0.22 (-0.95) | 0.07 (-0.95) | yes |
| reductive | defocus_blur | 0.41 (-0.59) | 0.26 (-0.54) | yes |

## Exploratory (no pre-registered prediction)
Shrink: fog 0.57/0.41, motion_blur 0.55/0.38, zoom_blur 0.59/0.41, pixelate 0.74/0.38, jpeg_compression 0.43/0.60, brightness ~0.95-0.97.
Grow: snow 1.17/1.33, frost 1.11/1.24, elastic_transform 1.07/1.12.

## Scale note (matters for G1/G3, untested)
Clean median payload: JPEG 9.9 kB, WebP 6.9 kB. Noise sev5: ~31-33 kB. Whether a ~20-25 kB difference matters for delivery time depends on uplink rate -> P1.

## Caveats
Single seed, 600 images; descriptive, not inferential. Erratum E1 (Gaussian blur not ImageNet-C) stands.
