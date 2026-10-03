#!/usr/bin/env python3
"""P68-R1 measured-trace ingestion + NETWORK-ONLY preflight.

Normalize one measured network trace into a canonical schema and report
time-order, missingness, sampling, throughput, and RTT diagnostics BEFORE any
inference-benefit G or routing-policy outcome is exposed.

The script intentionally does not read P2 benefit/prediction files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd


SIGMETRICS_UL_CANDIDATES = [
    "Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]",
    "ul_tput_mbps",
    "tput_ul",
    "throughput_mbps",
]
SIGMETRICS_DL_CANDIDATES = [
    "Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]",
    "dl_tput_mbps",
    "tput_dl",
    "throughput_mbps",
]
RTT_CANDIDATES = ["rtt_ms", "RTT", "rtt", "latency_ms", "ping_rtt_ms"]
TIME_CANDIDATES = ["utc_ts", "TIME_STAMP", "time", "local_dt", "timestamp", "datetime"]
OPERATOR_CANDIDATES = ["operator", "Operator", "carrier", "network_operator"]
RUN_CANDIDATES = ["run_id", "Run ID", "run", "drive_id"]
SEGMENT_CANDIDATES = ["segment_id", "Segment ID", "segment"]
TECH_CANDIDATES = ["actual_tech", "Event Technology", "technology", "tech"]
AREA_CANDIDATES = ["area", "Area", "region"]


def _find_col(df: pd.DataFrame, candidates: Iterable[str]) -> Optional[str]:
    cols = list(df.columns)
    exact = {str(c): c for c in cols}
    for c in candidates:
        if c in exact:
            return exact[c]
    lower = {str(c).strip().lower(): c for c in cols}
    for c in candidates:
        k = c.strip().lower()
        if k in lower:
            return lower[k]
    return None


def _require_col(df: pd.DataFrame, explicit: Optional[str], candidates: Iterable[str], what: str) -> str:
    if explicit:
        if explicit not in df.columns:
            raise ValueError(f"{what} column {explicit!r} not found. Available columns: {list(df.columns)}")
        return explicit
    c = _find_col(df, candidates)
    if c is None:
        raise ValueError(f"Could not infer {what} column. Supply it explicitly. Available columns: {list(df.columns)}")
    return c


def _parse_time(s: pd.Series) -> tuple[pd.Series, str]:
    numeric = pd.to_numeric(s, errors="coerce")
    numeric_fraction = float(numeric.notna().mean())
    if numeric_fraction >= 0.95:
        vals = numeric.astype(float)
        finite = vals[np.isfinite(vals)]
        if finite.empty:
            raise ValueError("Timestamp column has no finite values.")
        med_abs = float(np.nanmedian(np.abs(finite)))
        if med_abs > 1e17:
            vals = vals / 1e9
            kind = "numeric_ns_to_s"
        elif med_abs > 1e14:
            vals = vals / 1e6
            kind = "numeric_us_to_s"
        elif med_abs > 1e11:
            vals = vals / 1e3
            kind = "numeric_ms_to_s"
        else:
            kind = "numeric_s_or_relative"
        first = vals.dropna().iloc[0]
        return vals - first, kind

    dt = pd.to_datetime(s, errors="coerce", utc=True)
    if dt.notna().mean() < 0.95:
        raise ValueError(
            f"Timestamp parse failed for more than 5% of rows "
            f"(numeric parse={numeric_fraction:.3f}, datetime parse={dt.notna().mean():.3f})."
        )
    first = dt.dropna().iloc[0]
    return (dt - first).dt.total_seconds(), "datetime_to_elapsed_s"


def _as_str_col(df: pd.DataFrame, explicit: Optional[str], candidates: Iterable[str], default: str) -> pd.Series:
    if explicit and explicit not in df.columns:
        raise ValueError(f"Optional column {explicit!r} not found. Available columns: {list(df.columns)}")
    col = explicit if explicit else _find_col(df, candidates)
    if col is None:
        return pd.Series([default] * len(df), index=df.index, dtype="object")
    return df[col].astype("string").fillna(default)


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize(args: argparse.Namespace) -> tuple[pd.DataFrame, dict]:
    input_sha256 = _sha256(args.input_csv)
    input_size_bytes = Path(args.input_csv).stat().st_size
    if args.expected_sha256 and input_sha256.lower() != args.expected_sha256.lower():
        raise ValueError(f"Input SHA-256 mismatch: expected {args.expected_sha256}, got {input_sha256}")

    df = pd.read_csv(args.input_csv)
    if df.empty:
        raise ValueError("Input CSV is empty.")

    if args.source == "sigmetrics26":
        tcol = _require_col(df, args.timestamp_col, TIME_CANDIDATES, "timestamp")
        rcol = _require_col(df, args.rtt_col, RTT_CANDIDATES, "RTT")
        tcands = SIGMETRICS_UL_CANDIDATES if args.direction == "uplink" else SIGMETRICS_DL_CANDIDATES
        xcol = _require_col(df, args.throughput_col, tcands, f"{args.direction} throughput")
        documented_joint = True
    elif args.source in {"canonical", "pam2025"}:
        tcol = _require_col(df, args.timestamp_col, ["timestamp_s", *TIME_CANDIDATES], "timestamp")
        xcol = _require_col(df, args.throughput_col, ["throughput_mbps"], "throughput")
        rcol = _require_col(df, args.rtt_col, ["rtt_ms", *RTT_CANDIDATES], "RTT")
        documented_joint = bool(args.is_joint)
    else:
        raise ValueError(f"Unsupported source: {args.source}")

    elapsed, time_parse = _parse_time(df[tcol])
    throughput = pd.to_numeric(df[xcol], errors="coerce")
    rtt = pd.to_numeric(df[rcol], errors="coerce")

    out = pd.DataFrame({
        "source_family": args.source_family or args.source,
        "source_commit": args.source_commit or "",
        "campaign": args.campaign or "",
        "operator": _as_str_col(df, args.operator_col, OPERATOR_CANDIDATES, args.operator or ""),
        "run_id": _as_str_col(df, args.run_col, RUN_CANDIDATES, args.run_id or ""),
        "segment_id": _as_str_col(df, args.segment_col, SEGMENT_CANDIDATES, ""),
        "timestamp_s": elapsed,
        "throughput_mbps": throughput,
        "throughput_direction": args.direction,
        "rtt_ms": rtt,
        "tech": _as_str_col(df, args.tech_col, TECH_CANDIDATES, ""),
        "area": _as_str_col(df, args.area_col, AREA_CANDIDATES, ""),
        "is_joint": bool(documented_joint),
        "missing_reason": "",
        "source_file": str(args.input_csv),
    })

    m_t = out["throughput_mbps"].isna()
    m_r = out["rtt_ms"].isna()
    out.loc[m_t & m_r, "missing_reason"] = "throughput_and_rtt_missing"
    out.loc[m_t & ~m_r, "missing_reason"] = "throughput_missing"
    out.loc[~m_t & m_r, "missing_reason"] = "rtt_missing"

    meta = {
        "input_rows": int(len(df)),
        "input_sha256": input_sha256,
        "input_size_bytes": int(input_size_bytes),
        "timestamp_column": tcol,
        "throughput_column": xcol,
        "rtt_column": rcol,
        "time_parse": time_parse,
        "documented_joint": bool(documented_joint),
    }
    return out, meta


def _q(v: pd.Series, p: float) -> Optional[float]:
    a = pd.to_numeric(v, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    return None if a.empty else float(a.quantile(p))


def preflight(c: pd.DataFrame, meta: dict, gap_factor: float) -> dict:
    t = pd.to_numeric(c["timestamp_s"], errors="coerce")
    dt = t.diff()
    pos_dt = dt[dt > 0]
    med_dt = float(pos_dt.median()) if not pos_dt.empty else None
    gap_thr = (gap_factor * med_dt) if med_dt is not None else None
    x = pd.to_numeric(c["throughput_mbps"], errors="coerce")
    r = pd.to_numeric(c["rtt_ms"], errors="coerce")

    report = {
        **meta,
        "rows": int(len(c)),
        "valid_timestamp_share": float(t.notna().mean()),
        "duration_s": float(t.max() - t.min()) if t.notna().any() else None,
        "duplicate_timestamp_rows": int(t.duplicated(keep=False).sum()),
        "non_increasing_steps": int((dt <= 0).fillna(False).sum()),
        "median_positive_sample_interval_s": med_dt,
        "p95_positive_sample_interval_s": _q(pos_dt, 0.95),
        "long_gap_threshold_s": gap_thr,
        "long_gap_count": int((dt > gap_thr).sum()) if gap_thr is not None else None,
        "throughput_missing_share": float(x.isna().mean()),
        "throughput_nonpositive_share": float((x <= 0).fillna(False).mean()),
        "throughput_mbps_p05": _q(x, 0.05),
        "throughput_mbps_median": _q(x, 0.50),
        "throughput_mbps_p95": _q(x, 0.95),
        "rtt_missing_share": float(r.isna().mean()),
        "rtt_nonpositive_share": float((r <= 0).fillna(False).mean()),
        "rtt_ms_p05": _q(r, 0.05),
        "rtt_ms_median": _q(r, 0.50),
        "rtt_ms_p95": _q(r, 0.95),
        "joint_flag_share": float(c["is_joint"].astype(bool).mean()),
        "operator_count": int(c.loc[c["operator"].astype(str).ne(""), "operator"].nunique(dropna=True)),
        "run_count": int(c.loc[c["run_id"].astype(str).ne(""), "run_id"].nunique(dropna=True)),
        "segment_count": int(c.loc[c["segment_id"].astype(str).ne(""), "segment_id"].nunique(dropna=True)),
    }

    failures = []
    if report["valid_timestamp_share"] < 0.95:
        failures.append("timestamp_missing_gt_5pct")
    if report["non_increasing_steps"] > 0:
        failures.append("timestamps_not_strictly_increasing")
    if report["throughput_missing_share"] > 0.10:
        failures.append("throughput_missing_gt_10pct")
    if report["rtt_missing_share"] > 0.10:
        failures.append("rtt_missing_gt_10pct")
    if report["throughput_nonpositive_share"] > 0.10:
        failures.append("throughput_nonpositive_gt_10pct")
    if report["rtt_nonpositive_share"] > 0.10:
        failures.append("rtt_nonpositive_gt_10pct")

    report["preflight_status"] = "PASS" if not failures else "REVIEW"
    report["preflight_flags"] = failures
    report["confirmatory_outcomes_touched"] = False
    return report


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_csv", required=True)
    ap.add_argument("--source", choices=["sigmetrics26", "pam2025", "canonical"], required=True)
    ap.add_argument("--out_prefix", required=True)
    ap.add_argument("--direction", choices=["uplink", "downlink"], default="uplink")
    ap.add_argument("--source_family")
    ap.add_argument("--source_commit")
    ap.add_argument("--expected_sha256", help="Optional exact SHA-256 of the downloaded input file; mismatch aborts.")
    ap.add_argument("--campaign")
    ap.add_argument("--operator")
    ap.add_argument("--run_id")
    ap.add_argument("--timestamp_col")
    ap.add_argument("--throughput_col")
    ap.add_argument("--rtt_col")
    ap.add_argument("--operator_col")
    ap.add_argument("--run_col")
    ap.add_argument("--segment_col")
    ap.add_argument("--tech_col")
    ap.add_argument("--area_col")
    ap.add_argument("--is_joint", action="store_true",
                    help="For canonical/PAM input only: assert throughput and RTT are empirically aligned in supplied rows.")
    ap.add_argument("--gap_factor", type=float, default=5.0)
    args = ap.parse_args()

    canonical, meta = normalize(args)
    report = preflight(canonical, meta, args.gap_factor)

    prefix = Path(args.out_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    canonical_path = prefix.with_suffix(".canonical.csv")
    json_path = prefix.with_suffix(".preflight.json")
    csv_path = prefix.with_suffix(".preflight.csv")
    canonical.to_csv(canonical_path, index=False)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    pd.DataFrame([report]).to_csv(csv_path, index=False)
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"WROTE {canonical_path}")
    print(f"WROTE {json_path}")
    print(f"WROTE {csv_path}")


if __name__ == "__main__":
    main()
