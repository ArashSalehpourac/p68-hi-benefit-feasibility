import argparse
import importlib.util
import tempfile
import unittest
from pathlib import Path

import pandas as pd

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "trace_ingest_preflight.py"
spec = importlib.util.spec_from_file_location("trace_ingest_preflight", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class TracePreflightTests(unittest.TestCase):
    def _args(self, csv_path, source="sigmetrics26"):
        return argparse.Namespace(
            input_csv=str(csv_path), source=source, out_prefix=str(csv_path) + ".out",
            direction="uplink", source_family=None, source_commit="test",
            expected_sha256=None, campaign="synthetic", operator=None, run_id=None,
            timestamp_col=None, throughput_col=None, rtt_col=None, operator_col=None,
            run_col=None, segment_col=None, tech_col=None, area_col=None,
            is_joint=False, gap_factor=5.0,
        )

    def test_sigmetrics_autodetect_joint_uplink(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "trace.csv"
            pd.DataFrame({
                "utc_ts": [1000.0, 1000.2, 1000.4],
                "rtt_ms": [30.0, 40.0, 35.0],
                "operator": ["att"] * 3,
                "Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]": [10.0, 12.0, 11.0],
            }).to_csv(p, index=False)
            c, meta = mod.normalize(self._args(p))
            self.assertTrue(meta["documented_joint"])
            r = mod.preflight(c, meta, 5.0)
            self.assertEqual(r["preflight_status"], "PASS")
            self.assertFalse(r["confirmatory_outcomes_touched"])

    def test_canonical_nonmonotonic_is_review(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "trace.csv"
            pd.DataFrame({
                "timestamp_s": [0.0, 1.0, 0.5],
                "throughput_mbps": [10.0, 10.0, 10.0],
                "rtt_ms": [20.0, 20.0, 20.0],
            }).to_csv(p, index=False)
            a = self._args(p, source="canonical")
            a.is_joint = True
            c, meta = mod.normalize(a)
            r = mod.preflight(c, meta, 5.0)
            self.assertEqual(r["preflight_status"], "REVIEW")
            self.assertIn("timestamps_not_strictly_increasing", r["preflight_flags"])

    def test_expected_hash_mismatch_aborts(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "trace.csv"
            pd.DataFrame({
                "timestamp_s": [0.0, 1.0],
                "throughput_mbps": [10.0, 11.0],
                "rtt_ms": [20.0, 21.0],
            }).to_csv(p, index=False)
            a = self._args(p, source="canonical")
            a.expected_sha256 = "0" * 64
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                mod.normalize(a)


if __name__ == "__main__":
    unittest.main()
