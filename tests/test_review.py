from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from gtta import review, verification
from gtta.artifact import ARTIFACT_SCHEMA_VERSION
from gtta.cli import app
from gtta.review import (
    REVIEW_BUNDLE_VERSION,
    ReviewBundleInputError,
    build_review_bundle,
)


SOURCE_TEXT = "The synthetic consultation closes on 2026-09-15."


def artifact_payload(*, verify: bool = True) -> dict[str, object]:
    return {
        "schema_version": ARTIFACT_SCHEMA_VERSION,
        "artifact_id": "review-bundle-001",
        "title": "Synthetic consultation",
        "question": "Should the operator prepare a reversible response?",
        "decision": "Choose whether to prepare a limited response plan.",
        "audience": "Operating committee",
        "time_horizon": "30–90 days",
        "mode": "B",
        "evidence_mode": "illustrative source packet",
        "bottom_line": {
            "text": "Prepare a reversible response during review.",
            "claim_ids": ["c2"],
        },
        "claims": [
            {
                "claim_id": "c1",
                "text": "The consultation closes on 2026-09-15.",
                "kind": "fact",
                "provenance": "user-provided",
                "source_refs": ["notice"],
                "verify": verify,
                "confidence": "Moderate",
            },
            {
                "claim_id": "c2",
                "text": "A reversible response preserves options during review.",
                "kind": "assessment",
                "provenance": "analyst-judgment",
                "basis_claim_ids": ["c1"],
                "confidence": "Moderate",
            },
        ],
        "sections": {
            "actors": {
                "text": "The operator values reversibility during review.",
                "claim_ids": ["c1"],
            }
        },
        "options": [
            {
                "option_id": "o1",
                "title": "Prepare only",
                "benefit": "Preserves readiness.",
                "downside": "Uses limited staff time.",
                "conditions": "Do not act without review.",
                "basis_claim_ids": ["c1", "c2"],
            }
        ],
        "confidence": "Moderate",
        "key_unknowns": ["Whether the illustrative notice will change."],
        "change_conditions": ["Withdrawal of the illustrative notice."],
        "limitations": ["Synthetic source material only."],
    }


def source_catalog_payload() -> dict[str, object]:
    return {
        "schema_version": "gtta.sources@1.0",
        "sources": [
            {
                "source_id": "notice",
                "path": "sources/notice.md",
                "title": "Synthetic notice",
            }
        ],
        "quotes": [
            {
                "claim_id": "c1",
                "source_id": "notice",
                "text": "consultation closes on 2026-09-15",
            }
        ],
    }


def complete_check(packet: dict) -> dict:
    return {
        "implemented": True,
        "valid": True,
        "errors": [],
        "response": {
            "packet_status": "packet_complete",
            "claims": [],
            "owner_actions": [],
            "human_review_required": True,
            "factuality_status": "not_assessed",
        },
    }


def write_inputs(tmp_path: Path, *, verify: bool = True) -> Path:
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "notice.md").write_text(SOURCE_TEXT, encoding="utf-8")
    artifact_path = tmp_path / "memo.json"
    artifact_path.write_text(
        json.dumps(artifact_payload(verify=verify), indent=2), encoding="utf-8"
    )
    (tmp_path / "memo.sources.json").write_text(
        json.dumps(source_catalog_payload(), indent=2), encoding="utf-8"
    )
    return artifact_path


def stub_optional_renderers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        verification,
        "_load_agenda_dependencies",
        lambda: (complete_check, lambda path: path.read_text(encoding="utf-8")),
    )
    monkeypatch.setattr(
        review,
        "render_verification_markdown",
        lambda report: f"# Verification\n\nStatus: {report.packet_status}\n",
    )
    monkeypatch.setattr(
        review,
        "render_verification_html",
        lambda report: f"<html><body>{report.packet_status}</body></html>",
    )


def test_build_review_bundle_writes_versioned_auditable_outputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    artifact_path = write_inputs(tmp_path)
    stub_optional_renderers(monkeypatch)
    output_dir = tmp_path / "bundle"

    result = build_review_bundle(artifact_path, output_dir=output_dir)

    assert result.report.passed is True
    assert set(path.name for path in output_dir.iterdir()) == {
        "manifest.json",
        "memo.md",
        "repair.md",
        "review.html",
        "verification.json",
        "verification.md",
        "verification.sarif",
    }
    manifest = json.loads((output_dir / "manifest.json").read_text())
    assert manifest["interface"] == REVIEW_BUNDLE_VERSION
    assert manifest["verification_interface"] == "gtta.memo-verification@1.0"
    assert manifest["strict"] is True
    assert manifest["passed"] is True
    assert manifest["packet_status"] == "packet_complete"
    assert manifest["human_review_required"] is True
    assert manifest["inputs"]["artifact"]["artifact_id"] == "review-bundle-001"
    assert manifest["inputs"]["artifact"]["mode"] == "B"
    assert manifest["inputs"]["source_catalog"]["filename"] == "memo.sources.json"
    assert manifest["inputs"]["loaded_sources"] == [
        {
            "source_id": "notice",
            "sha256": hashlib.sha256(SOURCE_TEXT.encode()).hexdigest(),
        }
    ]
    for name, metadata in manifest["outputs"].items():
        assert hashlib.sha256((output_dir / name).read_bytes()).hexdigest() == metadata[
            "sha256"
        ]
    for name in (
        "manifest.json",
        "repair.md",
        "verification.json",
        "verification.sarif",
    ):
        assert SOURCE_TEXT not in (output_dir / name).read_text(encoding="utf-8")


def test_review_cli_writes_failure_bundle_and_exits_one(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    artifact_path = write_inputs(tmp_path, verify=False)
    stub_optional_renderers(monkeypatch)
    output_dir = tmp_path / "failed-review"

    result = CliRunner().invoke(
        app,
        ["review", str(artifact_path), "--out-dir", str(output_dir)],
    )

    assert result.exit_code == 1, result.output
    assert "REVIEW REQUIRED" in result.output
    manifest = json.loads((output_dir / "manifest.json").read_text())
    assert manifest["passed"] is False
    assert "GTTAV001" in (output_dir / "repair.md").read_text(encoding="utf-8")


def test_review_refuses_to_overwrite_an_existing_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    artifact_path = write_inputs(tmp_path)
    stub_optional_renderers(monkeypatch)
    output_dir = tmp_path / "existing"
    output_dir.mkdir()
    sentinel = output_dir / "keep.txt"
    sentinel.write_text("operator data", encoding="utf-8")

    with pytest.raises(ReviewBundleInputError, match="already exists"):
        build_review_bundle(artifact_path, output_dir=output_dir)

    assert sentinel.read_text(encoding="utf-8") == "operator data"
    assert list(output_dir.iterdir()) == [sentinel]


def test_review_write_failure_removes_staging_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    artifact_path = write_inputs(tmp_path)
    stub_optional_renderers(monkeypatch)
    output_dir = tmp_path / "atomic-review"
    original_write_text = Path.write_text

    def fail_while_writing_html(path: Path, data: str, **kwargs) -> int:
        if path.name == "review.html" and path.parent.name.startswith(
            ".atomic-review.tmp-"
        ):
            raise OSError("synthetic write failure")
        return original_write_text(path, data, **kwargs)

    monkeypatch.setattr(Path, "write_text", fail_while_writing_html)

    with pytest.raises(OSError, match="synthetic write failure"):
        build_review_bundle(artifact_path, output_dir=output_dir)

    assert not output_dir.exists()
    assert not list(tmp_path.glob(".atomic-review.tmp-*"))
