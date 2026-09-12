"""Integration contract against the real optional Agenda Intelligence package."""

from __future__ import annotations

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
