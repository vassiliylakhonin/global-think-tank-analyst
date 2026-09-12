"""Integration contract against the real optional Agenda Intelligence package."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from gtta.artifact import check_memo_artifact
from gtta.verification import load_source_catalog, verify_memo_artifact


ROOT = Path(__file__).resolve().parents[1]
COOKBOOK = ROOT / "examples" / "cookbooks" / "secondary-sanctions"


def test_pinned_agenda_1_9_checks_the_canonical_cookbook():
    agenda_intelligence = pytest.importorskip("agenda_intelligence")
    assert agenda_intelligence.__version__ == "1.9.0"
    artifact_report = check_memo_artifact(
        (COOKBOOK / "memo.json").read_text(encoding="utf-8")
    )
    assert artifact_report.artifact is not None, artifact_report.findings
    catalog = load_source_catalog(
        (COOKBOOK / "memo.sources.json").read_text(encoding="utf-8")
    )

    report = verify_memo_artifact(
        artifact_report.artifact,
        source_catalog=catalog,
        base_dir=COOKBOOK,
        strict=True,
    )

    assert report.passed is True
    assert report.packet_status == "packet_complete"
    assert report.agenda_result["response"]["factuality_status"] == "not_assessed"


def test_portable_verification_benchmark_passes(tmp_path: Path):
    pytest.importorskip("agenda_intelligence")
    summary_path = tmp_path / "summary.json"
    sarif_path = tmp_path / "benchmark.sarif"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_verification_benchmark.py",
            "--out",
            str(summary_path),
            "--sarif",
            str(sarif_path),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["passed"] is True
    assert summary["case_count"] == 6
    assert summary["golden_case_count"] == 2
    assert summary["negative_control_count"] == 4
    assert summary["source_inputs_unchanged"] is True
    sarif = json.loads(sarif_path.read_text(encoding="utf-8"))
    assert sarif["version"] == "2.1.0"
    assert not [item for item in sarif["runs"][0]["results"] if item["level"] == "error"]
    assert len([item for item in sarif["runs"][0]["results"] if item["level"] == "note"]) >= 4
