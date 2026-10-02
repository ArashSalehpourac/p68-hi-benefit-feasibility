# P68 — C1 window check vs T0 and G4(b) bias-sign test (2026-10-02)

Simulator p1_queue_sim_v2 (assumed network), 600-image P0 JPEG payloads, n=40,000/config, 15 configs, D = c*T0, c in {1.00,1.15,1.30,1.50,1.75}. Script scripts/p1_c1_g4b.py; output results/p1/p1_c1_g4b.csv (75 rows).

C1: proxy (in-window share >= 0.2 and coupling >= 0.05) holds for >= 3 contiguous c in 7/15 configs (11/15 on the fine ms grid); fails at load 0.85 and at 1 Mbit/s with load >= 0.6.
G4(a): excess ECE over null <= 0.0067 in all cells (threshold 0.02): does not fire.
G4(b): >15% of strata above null 95th pct in 5/75 cells; under an operational reading of "consistent sign" (>= 75% of exceeding strata share a sign; C2 gives no number, needs author confirmation) it fires in 1/75 cells (1 Mbit/s, load 0.85, c=1.75; mean bias +0.005). G4 does not fire overall.
