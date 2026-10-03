# P68-R1N — Sustained-warm remote-service freeze audit

Date: 2026-10-03
Status: **FAIL — FIXED REMOTE-SERVICE CONSTANT REJECTED**

## Protocol decision

R1N was the final permitted attempt to justify one fixed hardware-specific remote-service constant. It used:
- the 336-state exact P2-reproduction primary corpus;
- Tesla T4;
- batch-1 FP16-autocast service;
- fixed 120-s model-specific preconditioning;
- five randomized balanced rounds;
- unchanged R1M stability thresholds;
- no inference benefit, correctness, confidence, prediction, or policy outcome.

Exact P2 JPEG reproduction again passed: 336/336.

## Sustained-warm pooled timing

- ConvNeXt-Base + JPEG: p95 23.615 ms (bootstrap 95% CI 22.844–24.151);
- ConvNeXt-Base + WebP: p95 24.406 ms (23.821–25.031);
- ViT-B/16 + JPEG: p95 13.218 ms (12.901–13.515);
- ViT-B/16 + WebP: p95 14.847 ms (14.522–15.269).

## Unchanged stability gate

- ConvNeXt + JPEG: PASS (CV 0.0354; max/min 1.0802; CI relative width 0.0554).
- ConvNeXt + WebP: PASS (CV 0.0487; max/min 1.1264; CI relative width 0.0496).
- ViT-B/16 + WebP: PASS (CV 0.0670; max/min 1.1365; CI relative width 0.0504).
- ViT-B/16 + JPEG: **FAIL**. CV 0.0992 passes narrowly, but max/min = 1.2161 exceeds the frozen 1.20 limit.

Therefore ALL FOUR ARMS PASS = false.

## Consequence

Per the pre-specified R1N rule:
- do not loosen the threshold;
- do not drop a round;
- do not freeze a fixed p95 service constant;
- do not freeze an E2E grid by adding one service constant to the network budget.

R2 must carry remote-service latency as an **empirical model×codec distribution**. The R1N raw sustained-warm samples are the primary service distribution; R1M-v2 impulse timings remain a sensitivity only.

The next outcome-blind step is to combine the frozen measured PAM network component with the empirical R1N service distributions and verify a non-saturated end-to-end deadline region before inference benefit G is loaded.