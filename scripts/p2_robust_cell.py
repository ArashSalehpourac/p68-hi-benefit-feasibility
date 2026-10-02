# ===== P2 robustness cell (append after the analysis cell; needs D, META, IMAGES, MODELS, one_image, predict, within_cov, boot_ci, PAIRS, FAMILIES, CONDS in memory) =====
# (1) Local model on the SAME JPEG-decoded pixels as the remote (removes raw-vs-JPEG asymmetry), 20 images/class subset, same corrupted inputs (deterministic seeds).
# (2) Pooled vs within-stratum correlation of G with bytes, to show where the coupling lives.
SUB = META.groupby("label").head(int(globals().get("ROBUST_PER_CLASS", 20))).image_idx.to_numpy()
parts = []
for s in range(0, len(SUB), 50):
    ids = SUB[s:s + 50]
    res = Parallel(n_jobs=N_JOBS)(delayed(one_image)(int(i), IMAGES[i]) for i in ids)
    dec = np.stack([d for r in res for (_, _, _, _, d) in r])
    df = pd.DataFrame({"image_idx": np.repeat(ids, len(CONDS)), "label": np.repeat(META.label.to_numpy()[ids], len(CONDS)),
                       "corruption": [c for r in res for (c, _, _, _, _) in r], "severity": [sv for r in res for (_, sv, _, _, _) in r],
                       "bytes": [b for r in res for (_, _, b, _, _) in r]})
    for n in sorted({m for p in PAIRS.values() for m in p}):
        df[f"{n}_predJ"], _ = predict(MODELS[n], dec)
    parts.append(df)
RJ = pd.concat(parts, ignore_index=True)
RJ = RJ.merge(D[["image_idx", "corruption", "severity"] + [f"{n}_pred" for n in MODELS]], on=["image_idx", "corruption", "severity"], how="left")
rob = []
for pair, (L, R) in PAIRS.items():
    okR = (RJ[f"{R}_predJ"] == RJ["label"]).astype(int)
    RJ[f"G_rawlocal_{pair}"] = okR - (RJ[f"{L}_pred"] == RJ["label"]).astype(int)      # as in the main run (local sees raw)
    RJ[f"G_jpeglocal_{pair}"] = okR - (RJ[f"{L}_predJ"] == RJ["label"]).astype(int)    # local sees the same JPEG-decoded pixels
    for fam in ["additive", "reductive"]:
        sub = RJ[RJ.corruption.isin([c for c, f in FAMILIES.items() if f == fam])]
        for lab in ["rawlocal", "jpeglocal"]:
            g = f"G_{lab}_{pair}"; cov, corr = within_cov(sub, g); lo, hi = boot_ci(sub, g, B=200)
            rob.append(dict(pair=pair, family=fam, local_input=lab, within_cov=cov, within_corr=corr, ci_lo=lo, ci_hi=hi, n_images=len(SUB)))
ROB = pd.DataFrame(rob); print(ROB.round(4).to_string(index=False))
dec_rows = []
for pair in PAIRS:
    for fam in ["additive", "reductive"]:
        sub = D[D.corruption.isin([c for c, f in FAMILIES.items() if f == fam])]
        g = sub[f"G_{pair}"].to_numpy(float); b = sub["bytes"].to_numpy(float)
        cm = sub.groupby(["corruption", "severity"]).agg(G=(f"G_{pair}", "mean"), B=("bytes", "mean"))
        dec_rows.append(dict(pair=pair, family=fam, pooled_corr_G_bytes=np.corrcoef(g, b)[0, 1],
                             between_cell_corr_G_bytes=np.corrcoef(cm.G, cm.B)[0, 1],
                             within_corr=within_cov(sub, f"G_{pair}")[1]))
DEC = pd.DataFrame(dec_rows); print(DEC.round(4).to_string(index=False))
ROB.to_csv(f"{OUT_DIR}/summary_p2_robust_localJPEG.csv", index=False); DEC.to_csv(f"{OUT_DIR}/summary_p2_pooled_vs_within.csv", index=False)
print("saved robustness tables")
