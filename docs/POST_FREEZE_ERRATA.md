# P68 post-freeze errata and change log

`proposal_v4_final.md` (SHA-256 3d40c2d32394127cc99f8244490a83a9fd266806edd5891f7bf28d3854f89b73) is left byte-for-byte unchanged. Amendments are recorded here.

## 2026-10-01 — E1: "Gaussian blur" is not an ImageNet-C corruption
- v4-final §4 lists defocus blur, **Gaussian blur** and contrast as the confirmatory reductive family.
- The 15 ImageNet-C corruptions are: gaussian_noise, shot_noise, impulse_noise, defocus_blur, glass_blur, motion_blur, zoom_blur, snow, frost, fog, brightness, contrast, elastic_transform, pixelate, jpeg_compression. There is no Gaussian blur.
- Amendment: the confirmatory reductive family is **defocus_blur and contrast**. Motion/zoom blur remain exploratory. If a Gaussian-blur arm is wanted it must be added as a separately labeled, non-ImageNet-C corruption before any real data are looked at.
- Reason: found while writing the P0 notebook (before any real-data run). Implemented in P68_P0_payload_pilot.ipynb.

## 2026-10-01 — E2: P0 notebook added
- File: P68_P0_payload_pilot.ipynb (Colab). Smoke-tested only on synthetic images in a local Python environment (not in Colab, not on real images). Verified there: 15 corruption values present, 0 failed rows, 10/10 confirmatory rows matched the predicted size direction on synthetic images (this is NOT evidence).
- A bug found in testing: fog failed inside parallel workers because the NumPy-2 shim was only applied in the parent process. Fixed (shim re-applied in the worker) and a warning prints if any corruption has failed rows.
- Unverified and untested: the Hugging Face dataset id `ILSVRC/imagenet-1k` and streaming behavior; the Imagenette URL; the GitHub-push cell (uses a Colab secret, never printed). Colab secret names default to HF_TOKEN and GITHUB_TOKEN.
- SOURCE="imagenette" and "synthetic" runs are not protocol evidence.
