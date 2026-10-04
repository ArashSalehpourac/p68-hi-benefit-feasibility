# P68-R3 — SESOI / equivalence rule (DRAFT — AWAITING AUTHOR CONFIRMATION)

Date: 2026-10-04
Status: **NOT FROZEN**

R3 is confirmatory and must not be executed until this rule is explicitly author-confirmed.

## Historical threshold retained

The post-rejection protocol already recorded the candidate judgment:
- material absolute improvement: **>= 2.0 percentage points**;
- strong improvement: **>= 4.0 percentage points**;
- and **>= 20% of recoverable class-tail benefit**.

R2 was completed before any R3 policy comparison.

## Recommended operational definition

Primary endpoint: paired difference in **deadline-adjusted top-1 accuracy** between joint and factorized policies at the same offload count, evaluated on held-out image/trace blocks at the frozen 95-ms deadline.

Primary material-superiority rule:
- `Delta_acc = Acc_joint - Acc_factorized >= +2.0 pp`, and
- the joint policy recovers at least 20% of the factorized-to-oracle class-tail headroom defined below.

Strong superiority: `Delta_acc >= +4.0 pp` with the same tail-recovery requirement.

Equivalence margin for the primary accuracy endpoint: **[-2.0 pp, +2.0 pp]**, using the same 2-pp minimally important difference rather than introducing a new post hoc margin.

## Class-tail endpoint

Define class-tail accuracy as the mean deadline-adjusted accuracy over the worst 20% of ImageNet classes, where the tail set is identified from the local-only baseline inside each training fold and then applied unchanged to the held-out fold.

Let:
- `Tail_F` = factorized-policy tail accuracy;
- `Tail_J` = joint-policy tail accuracy;
- `Tail_O` = oracle-realized-benefit ceiling tail accuracy.

Recoverable tail headroom is `Tail_O - Tail_F`.

Recovered fraction is `(Tail_J - Tail_F) / (Tail_O - Tail_F)` when the denominator is positive.

If `Tail_O - Tail_F <= 0`, the 20% tail-recovery condition is declared not applicable for that fold and cannot be used to claim superiority.

## Matched-budget rule

Primary: same offload count. The common offload count is chosen inside training/validation only; held-out evaluation uses rank-based top-K selection so factorized and joint policies invoke the remote model exactly the same number of times.

Secondary: matched transmitted-byte budget.

## Confirmatory interpretation

- Material joint advantage: both the +2 pp accuracy SESOI and 20% recoverable-tail rule are met with paired uncertainty supporting the direction.
- Strong joint advantage: +4 pp accuracy and the tail rule.
- Operational equivalence: the paired 95% CI for `Delta_acc` lies wholly inside [-2 pp,+2 pp], with no reproducible tail advantage meeting the 20% rule.
- Otherwise: inconclusive / budget- or regime-dependent.

## Required author action

Explicitly confirm this rule before R3 execution. Until confirmation, no joint-vs-factorized policy outcomes may be computed.