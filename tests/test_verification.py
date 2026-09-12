from __future__ import annotations

import json
from pathlib import Path

import pytest

from gtta.artifact import ARTIFACT_SCHEMA_VERSION, MemoArtifact, check_memo_artifact
from gtta.verification import (
    MemoSourceCatalog,
    VerificationInputError,
    build_evidence_packet,
    get_memo_source_catalog_schema,
    load_source_catalog,
    render_memo_repair_prompt,
    verify_memo_artifact,
)


def sourced_mode_b(*, verify: bool = True) -> dict[str, object]:
    return {
        "schema_version": ARTIFACT_SCHEMA_VERSION,
        "artifact_id": "policy-notice-001",
        "title": "Synthetic policy notice",
        "question": "Should the operator prepare a reversible response?",
        "decision": "Choose whether to prepare a limited response plan.",
        "audience": "Operating committee",
        "time_horizon": "30–90 days",
        "mode": "B",
        "evidence_mode": "illustrative source packet",
        "bottom_line": {
            "text": "Prepare a reversible response while the notice is reviewed.",
            "claim_ids": ["c2"],
        },
        "claims": [
            {
                "claim_id": "c1",
                "text": "The synthetic consultation closes on 2026-09-15.",
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
                "conditions": "Do not act on the synthetic notice without review.",
                "basis_claim_ids": ["c1", "c2"],
            }
        ],
        "confidence": "Moderate",
        "key_unknowns": ["Whether the illustrative notice will change."],
        "change_conditions": ["Withdrawal of the illustrative notice."],
        "limitations": ["Synthetic source material only."],
    }


def parsed_artifact(*, verify: bool = True) -> MemoArtifact:
    report = check_memo_artifact(sourced_mode_b(verify=verify))
    assert report.artifact is not None, report.findings
    return report.artifact


def complete_check(packet: dict) -> dict:
    return {
        "implemented": True,
        "valid": True,
        "errors": [],
        "response": {
            "packet_status": "packet_complete",
            "owner_actions": [],
            "human_review_required": True,
        },
    }


def incomplete_check(packet: dict) -> dict:
    return {
        "implemented": True,
        "valid": True,
        "errors": [],
        "response": {
            "packet_status": "packet_incomplete",
            "claims": [
                {
                    "claim_id": "c1",
                    "packet_status": "packet_incomplete",
                    "issues": ["missing_source:notice"],
                }
            ],
            "owner_actions": ["Supply the missing source notice."],
            "human_review_required": True,
        },
    }


def source_catalog() -> MemoSourceCatalog:
    return load_source_catalog(
        {
            "schema_version": "gtta.sources@1.0",
            "sources": [
                {
                    "source_id": "notice",
                    "path": "sources/notice.md",
                    "title": "Synthetic notice",
                },
                {
                    "source_id": "unused",
                    "path": "sources/unused.md",
                },
            ],
            "quotes": [
                {
                    "claim_id": "c1",
                    "source_id": "notice",
                    "text": "consultation closes on 2026-09-15",
                }
            ],
        }
    )


def test_source_catalog_schema_is_versioned_and_public():
    schema = get_memo_source_catalog_schema()
    assert schema["title"] == "MemoSourceCatalog"
    assert schema["$id"] == "urn:gtta:schema:sources:1.0"
    assert "gtta.sources@1.0" in json.dumps(schema)
    assert "schema_version" in schema["required"]
    assert schema == MemoSourceCatalog.model_json_schema()


def test_projection_selects_source_backed_claims_and_used_sources(tmp_path: Path):
    loaded: list[Path] = []

    def load(path: Path) -> str:
        loaded.append(path)
        return "The synthetic consultation closes on 2026-09-15."

    packet = build_evidence_packet(
        parsed_artifact(),
        source_catalog=source_catalog(),
        base_dir=tmp_path,
        source_loader=load,
    )

    assert [claim["claim_id"] for claim in packet["claims"]] == ["c1"]
    assert packet["claims"][0]["source_ids"] == ["notice"]
    assert packet["claims"][0]["quotes"][0]["source_id"] == "notice"
    assert [source["source_id"] for source in packet["sources"]] == ["notice"]
    assert loaded == [(tmp_path / "sources" / "notice.md").resolve()]


def test_strict_verification_fails_closed_on_missing_verify_marker(tmp_path: Path):
    report = verify_memo_artifact(
        parsed_artifact(verify=False),
        source_catalog=source_catalog(),
        base_dir=tmp_path,
        strict=True,
        checker=complete_check,
        source_loader=lambda _: "The synthetic consultation closes on 2026-09-15.",
    )

    assert report.passed is False
    assert report.packet_status == "packet_complete"
    assert [finding.rule_id for finding in report.findings] == ["GTTAV001"]
    assert "source text" not in json.dumps(report.to_dict())


def test_non_strict_verification_reports_marker_gap_without_failing(tmp_path: Path):
    report = verify_memo_artifact(
        parsed_artifact(verify=False),
        source_catalog=source_catalog(),
        base_dir=tmp_path,
        strict=False,
        checker=complete_check,
        source_loader=lambda _: "The synthetic consultation closes on 2026-09-15.",
    )

    assert report.passed is True
    assert report.findings


def test_repair_prompt_is_bounded_and_does_not_repeat_source_text(tmp_path: Path):
    source_text = "The synthetic consultation closes on 2026-09-15."
    report = verify_memo_artifact(
        parsed_artifact(verify=False),
        source_catalog=source_catalog(),
        base_dir=tmp_path,
        strict=True,
        checker=incomplete_check,
        source_loader=lambda _: source_text,
    )

    prompt = render_memo_repair_prompt(report)

    assert "Never invent a source ID" in prompt
    assert "GTTAV001" in prompt
    assert "missing_source:notice" in prompt
    assert "stop and request the missing source" in prompt
    assert source_text not in prompt


def test_projection_rejects_source_path_escape(tmp_path: Path):
    artifact = parsed_artifact()
    catalog = source_catalog()
    catalog.sources[0].path = "../outside.md"

    with pytest.raises(VerificationInputError, match="must stay inside"):
        build_evidence_packet(
            artifact,
            source_catalog=catalog,
            base_dir=tmp_path,
            source_loader=lambda _: "x",
        )


def test_source_catalog_rejects_duplicate_ids():
    with pytest.raises(VerificationInputError, match="source_id values must be unique"):
        load_source_catalog(
            {
                "schema_version": "gtta.sources@1.0",
                "sources": [
                    {"source_id": "s1", "path": "one.txt"},
                    {"source_id": "s1", "path": "two.txt"},
                ],
            }
        )


def test_cli_verify_runs_through_the_composition_seam(tmp_path: Path, monkeypatch):
    from typer.testing import CliRunner

    from gtta.cli import app
    from gtta import verification

    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "notice.md").write_text(
        "The synthetic consultation closes on 2026-09-15.", encoding="utf-8"
    )
    artifact_path = tmp_path / "memo.json"
    artifact_path.write_text(json.dumps(sourced_mode_b()), encoding="utf-8")
    catalog_path = tmp_path / "memo.sources.json"
    catalog_path.write_text(
        json.dumps(source_catalog().model_dump(mode="json")), encoding="utf-8"
    )

    monkeypatch.setattr(
        verification,
        "_load_agenda_dependencies",
        lambda: (complete_check, lambda path: path.read_text(encoding="utf-8")),
    )
    result = CliRunner().invoke(
        app, ["verify", str(artifact_path), "--strict", "--format", "json"]
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["passed"] is True
    assert payload["packet_status"] == "packet_complete"
    assert payload["projected_claim_ids"] == ["c1"]


def test_cli_verify_writes_repair_prompt_on_strict_failure(
    tmp_path: Path, monkeypatch
):
    from typer.testing import CliRunner

    from gtta import verification
    from gtta.cli import app

    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    source_text = "The synthetic consultation closes on 2026-09-15."
    (source_dir / "notice.md").write_text(source_text, encoding="utf-8")
    artifact_path = tmp_path / "memo.json"
    artifact_path.write_text(
        json.dumps(sourced_mode_b(verify=False)), encoding="utf-8"
    )
    (tmp_path / "memo.sources.json").write_text(
        json.dumps(source_catalog().model_dump(mode="json")), encoding="utf-8"
    )
    repair_path = tmp_path / "repair.md"

    monkeypatch.setattr(
        verification,
        "_load_agenda_dependencies",
        lambda: (incomplete_check, lambda path: path.read_text(encoding="utf-8")),
    )
    result = CliRunner().invoke(
        app,
        [
            "verify",
            str(artifact_path),
            "--strict",
            "--repair-prompt",
            str(repair_path),
        ],
    )

    assert result.exit_code == 1, result.output
    prompt = repair_path.read_text(encoding="utf-8")
    assert "GTTA Memo Repair Instructions" in prompt
    assert "gtta verify memo.json --strict" in prompt
    assert source_text not in prompt
