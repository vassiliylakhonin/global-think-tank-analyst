import hashlib
import json
import socket
from pathlib import Path

import pytest
from typer.testing import CliRunner

from gtta.cli import app
from gtta.discipline import check_contract
from gtta.harvest import extract_text, harvest, load_snapshots, _public_address
from gtta.contract_v2 import ReversalCondition

REVERSAL = {
    "metric": "pilot loss",
    "operator": ">=",
    "threshold": 10.0,
    "unit": "USD",
    "review_by": "2026-12-01",
    "action": "Pause the pilot.",
}
MEMO = """Evidence mode: user-provided sources
[primary] The pilot has a capped budget. [SRC-01]
[analyst-judgment] Use a reversible pilot.
Confidence: Moderate.
Null hypothesis: If no action is taken, retain the existing operating posture.
"""


def codes(report):
    return {f.rule_id for f in report.findings}


def capture_fixture(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "gtta.harvest.fetch_https",
        lambda url: (
            b"<p>The pilot has a capped budget.</p><script>hidden</script>",
            "text/html; charset=utf-8",
            url,
        ),
    )
    harvest("https://example.org/", tmp_path)
    return tmp_path / "sources.json"


def test_capture_and_offline_literal_quote(monkeypatch, tmp_path):
    manifest = capture_fixture(monkeypatch, tmp_path)
    payload = json.loads(manifest.read_text())
    source = payload["sources"][0]
    assert source["retrieved_at"].endswith("Z")
    assert source["sha256"] != source["text_sha256"]
    assert load_snapshots(manifest) == {"SRC-01": "The pilot has a capped budget."}
    quotes = (
        "\n```gtta-quotes\n"
        + json.dumps([{"source_id": "SRC-01", "quote": "a capped budget"}])
        + "\n```\n"
    )
    report = check_contract(MEMO + quotes, mode="A", sources=manifest)
    assert report.passed
    assert report.ruleset_version == "gtta-method-contract@2.0.0"
    assert "GTTA014" in codes(
        check_contract(MEMO + quotes.replace("capped", "unlimited"), sources=manifest)
    )
    assert "GTTA015" in codes(check_contract(MEMO + quotes, strict=True))


def test_hash_tampering_and_missing_snapshot(monkeypatch, tmp_path):
    manifest = capture_fixture(monkeypatch, tmp_path)
    source = json.loads(manifest.read_text())["sources"][0]
    path = tmp_path / (source["sha256"] + ".raw")
    path.write_bytes(b"tampered")
    assert "GTTA015" in codes(check_contract(MEMO, sources=manifest))
    path.unlink()
    assert "GTTA015" in codes(check_contract(MEMO, sources=manifest))


def test_text_cannot_be_forged_independently_of_raw(monkeypatch, tmp_path):
    manifest = capture_fixture(monkeypatch, tmp_path)
    payload = json.loads(manifest.read_text())
    forged = b"Forged quote."
    digest = hashlib.sha256(forged).hexdigest()
    (tmp_path / (digest + ".txt")).write_bytes(forged)
    payload["sources"][0]["text_sha256"] = digest
    manifest.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="does not match"):
        load_snapshots(manifest)


def test_duplicate_source_is_not_overwritten(monkeypatch, tmp_path):
    manifest = capture_fixture(monkeypatch, tmp_path)
    old = manifest.read_bytes()
    with pytest.raises(ValueError, match="already exists"):
        harvest("https://example.org/", tmp_path)
    assert manifest.read_bytes() == old
    harvest("https://example.org/other", tmp_path, "SRC-02")
    assert len(load_snapshots(manifest)) == 2


@pytest.mark.parametrize(
    "url",
    [
        "http://example.org",
        "file:///etc/passwd",
        "https://user:pass@example.org",
        "https://example.org:444",
    ],
)
def test_unsafe_url_schemes_and_credentials_are_rejected(url):
    with pytest.raises(ValueError):
        _public_address(url)


@pytest.mark.parametrize(
    "address", ["127.0.0.1", "10.0.0.2", "169.254.169.254", "::1", "::ffff:127.0.0.1"]
)
def test_private_dns_is_rejected(monkeypatch, address):
    monkeypatch.setattr(
        socket,
        "getaddrinfo",
        lambda *a, **kw: [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (address, 443))],
    )
    with pytest.raises(ValueError, match="non-global"):
        _public_address("https://example.org")


def test_unknown_source_and_invalid_manifest_fail(monkeypatch, tmp_path):
    manifest = capture_fixture(monkeypatch, tmp_path)
    assert "GTTA015" in codes(
        check_contract(MEMO.replace("SRC-01", "SRC-99"), sources=manifest)
    )
    manifest.write_text('{"sources": []}')
    assert "GTTA015" in codes(check_contract(MEMO, sources=manifest))


def test_strict_is_opt_in_and_null_requires_body():
    legacy = check_contract("Evidence mode: reasoning-only\n[analyst-judgment] Wait.")
    assert legacy.passed
    strict = check_contract(
        "Evidence mode: reasoning-only\n[analyst-judgment] Wait.\n## Null hypothesis",
        strict=True,
    )
    assert "GTTA011" in codes(strict)
    assert "GTTA011" not in codes(check_contract(MEMO, strict=True))
    assert "GTTA011" in codes(
        check_contract(
            MEMO.replace(
                "Null hypothesis: If no action is taken, retain the existing operating posture.",
                "Null hypothesis: [fill in the baseline]",
            ),
            strict=True,
        )
    )
    assert "GTTA011" in codes(
        check_contract(
            "```\nNull hypothesis: This is merely a code example, not a baseline.\n```",
            strict=True,
        )
    )
    assert "GTTA011" not in codes(
        check_contract("Evidence mode: reasoning-only", mode="F", strict=True)
    )


def test_declared_fact_requires_reference_in_same_table_cell():
    text = MEMO + "\n| [primary] The pilot has a capped budget. | [SRC-01] |\n"
    report = check_contract(text, strict=True)
    assert "GTTA012" in codes(report)
    assert "GTTA012" in codes(
        check_contract(MEMO.replace("[SRC-01]", "[SRC-1]"), strict=True)
    )
    assert "GTTA012" not in codes(check_contract(MEMO, strict=True))
    assert "GTTA012" in codes(
        check_contract(MEMO + "\n> [primary] A fact with no reference.", strict=True)
    )


def test_structured_reversals_require_real_typed_fields():
    block = "\n```gtta-reversals\n" + json.dumps([REVERSAL]) + "\n```\n"
    assert "GTTA013" not in codes(check_contract(MEMO + block, mode="B", strict=True))
    assert "GTTA013" in codes(check_contract(MEMO, mode="B", strict=True))
    for bad in [
        [],
        [{}],
        [{**REVERSAL, "threshold": "ten"}],
        [{**REVERSAL, "threshold": True}],
        [{**REVERSAL, "review_by": "2026-02-30"}],
        [{**REVERSAL, "operator": "approximately"}],
    ]:
        text = MEMO + "\n```gtta-reversals\n" + json.dumps(bad) + "\n```\n"
        assert "GTTA013" in codes(check_contract(text, strict=True))
    assert "GTTA013" in codes(check_contract(MEMO + block.rstrip()[:-3], strict=True))
    with pytest.raises(ValueError):
        ReversalCondition.model_validate({**REVERSAL, "threshold": float("nan")})


def test_cli_harvest_and_check(monkeypatch, tmp_path):
    capture_fixture(monkeypatch, tmp_path / "captures")
    memo = tmp_path / "memo.md"
    memo.write_text(MEMO)
    result = CliRunner().invoke(
        app,
        [
            "check-contract",
            str(memo),
            "--sources",
            str(tmp_path / "captures/sources.json"),
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    assert json.loads(result.output)["passed"]
    memo.write_text(MEMO.replace("[SRC-01]", ""))
    result = CliRunner().invoke(
        app, ["check-contract", str(memo), "--strict", "--format", "sarif"]
    )
    assert result.exit_code == 1, result.output
    sarif = json.loads(result.output)
    assert any(item["ruleId"] == "GTTA012" for item in sarif["runs"][0]["results"])
    result = CliRunner().invoke(
        app, ["harvest", "https://example.org", "--out", str(tmp_path / "new")]
    )
    assert result.exit_code == 0, result.output
    assert json.loads(result.output)["source_id"] == "SRC-01"


def test_artifact_optional_fields_roundtrip():
    from test_artifact import valid_mode_b
    from gtta.artifact import check_memo_artifact, render_memo_artifact

    payload = valid_mode_b()
    assert not check_memo_artifact(payload, strict=True).passed
    payload.update(
        schema_version="gtta.memo@2.0",
        null_hypothesis="If nothing changes, retain the current operating posture.",
        reversal_conditions=[REVERSAL],
    )
    report = check_memo_artifact(payload, strict=True)
    assert report.passed
    rendered = render_memo_artifact(report.artifact)
    assert check_contract(rendered, mode="B", strict=True).passed
