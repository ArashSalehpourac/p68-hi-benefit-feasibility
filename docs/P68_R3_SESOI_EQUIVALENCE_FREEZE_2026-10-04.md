# P68-R3 — SESOI / equivalence rule (FROZEN)

Date: 2026-10-04  
Status: **FROZEN BEFORE R3 POLICY OUTCOMES**

Author confirmation received in project chat on 2026-10-04: **"freeze R3 rule"**.

R2 was completed before any R3 joint-vs-factorized policy comparison. The R2 provenance explicitly records that the policy benchmark had not yet been executed.

## 1. Primary endpoint and estimand

Primary endpoint: paired difference in **deadline-adjusted top-1 accuracy** between the joint and factorized policies at the same offload count, evaluated on held-out image/trace blocks at the frozen **95-ms** E2E deadline.

Define:

`Delta_acc = Acc_joint - Acc_factorized`.

## 2. Frozen SESOI

Material joint-policy superiority requires:

- `Delta_acc >= +2.0 percentage points`; **and**
- the joint policy recovers at least **20% of the factorized-to-oracle class-tail headroom**.

Strong superiority requires:

- `Delta_acc >= +4.0 percentage points`; **and**
- the same >=20% class-tail recovery condition.

The **2.0-pp** threshold is the minimally important absolute difference. The **4.0-pp** threshold is the strong-effect threshold.

## 3. Frozen equivalence margin

The primary accuracy equivalence margin is:

**[-2.0 pp, +2.0 pp]**

Operational equivalence requires the paired 95% CI for `Delta_acc` to lie wholly inside this interval and no reproducible class-tail advantage meeting the 20% rule.

## 4. Frozen class-tail endpoint

Class-tail accuracy is the mean deadline-adjusted accuracy over the **worst 20% of ImageNet classes**.

For every outer evaluation fold:

1. identify the tail set from **local-only accuracy in the training portion only**;
2. freeze that tail set;
3. apply it unchanged to the held-out fold.

Let:

- `Tail_F` = factorized-policy tail accuracy;
- `Tail_J` = joint-policy tail accuracy;
- `Tail_O` = oracle-realized-benefit ceiling tail accuracy.

Recoverable tail headroom:

`Tail_O - Tail_F`.

Recovered fraction:

`(Tail_J - Tail_F) / (Tail_O - Tail_F)`

when the denominator is positive.

If `Tail_O - Tail_F <= 0`, the 20% tail-recovery condition is **not applicable** for that fold and cannot be used to claim superiority.

## 5. Frozen matched-budget rule

Primary comparison: **same offload count**.

The common offload count is selected using training/validation data only. Held-out evaluation uses rank-based top-K selection so factorized and joint policies invoke the remote model exactly the same number of times.

Secondary comparison: **matched transmitted-byte budget**.

Remote-compute invocation count is reported separately.

## 6. Frozen interpretation

- **Material joint advantage:** +2 pp SESOI met, >=20% recoverable-tail rule met, and paired uncertainty supports the direction.
- **Strong joint advantage:** +4 pp threshold met, >=20% recoverable-tail rule met, and paired uncertainty supports the direction.
- **Operational equivalence:** paired 95% CI for `Delta_acc` lies wholly inside [-2,+2] pp and no reproducible tail advantage meets the 20% rule.
- **Otherwise:** inconclusive / budget- or regime-dependent.

## 7. Sequential-design lock

No SESOI, equivalence margin, tail definition, or interpretation rule may be changed after R3 policy outcomes are computed.

Any later alternative margin or tail definition must be labeled exploratory/sensitivity and cannot replace this confirmatory rule.
