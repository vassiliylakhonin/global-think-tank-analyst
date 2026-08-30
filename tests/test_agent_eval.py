import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "agent_eval.py"
PUBLISHED_RUN = (
    ROOT
    / "evals"
    / "agent-eval"
    / "runs"
    / "2026-08-30-antigravity-gemini-3.7-flash-high"
)


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_benchmark_cases_validate():
    result = _run("validate")
    assert result.returncode == 0, result.stderr
    assert "12 benchmark cases" in result.stdout


def test_harness_has_no_model_or_network_client():
    source = SCRIPT.read_text(encoding="utf-8")
    for forbidden in (
        "import openai",
        "from openai",
        "import anthropic",
        "from anthropic",
        "import requests",
        "urllib.request",
    ):
        assert forbidden not in source


def test_prepare_and_score_structural_comparison(tmp_path):
    run_dir = tmp_path / "run"
    prepared = _run("prepare", str(run_dir), "--seed", "7")
    assert prepared.returncode == 0, prepared.stderr

    requests = [
        json.loads(line)
        for line in (run_dir / "requests.jsonl").read_text().splitlines()
    ]
    mapping = json.loads((run_dir / "private-mapping.json").read_text())
    assert len(requests) == 24
    assert all("arm" not in request for request in requests)
    assert mapping["case_count"] == 12
    antigravity_manifest = json.loads(
        (run_dir / "antigravity-manifest.json").read_text()
    )
    assert len(antigravity_manifest) == 24
    assert all("arm" not in row for row in antigravity_manifest)
    assert len(list((run_dir / "antigravity-tasks").glob("[0-9]*.md"))) == 24

    outputs = []
    for sample in mapping["samples"]:
        evidence_mode = sample["evidence_mode"]
        if sample["arm"] == "skill":
            output = (
                f"Evidence mode: {evidence_mode}.\n"
                "[inference] A bounded input.\n"
                "[analyst-judgment] A bounded judgment.\n"
                "Confidence: Moderate."
            )
        else:
            output = f"Evidence mode: {evidence_mode}.\nConfidence: Moderate."
        outputs.append({"sample_id": sample["sample_id"], "output": output})

    response_dir = run_dir / "antigravity-responses"
    for row in outputs:
        (response_dir / f"{row['sample_id']}.md").write_text(
            row["output"], encoding="utf-8"
        )
    metadata_path = run_dir / "run-metadata.input.json"
    metadata_path.write_text(
        json.dumps(
            {
                "runner": "Antigravity",
                "app_version": "2.11.0",
                "model": "test-model",
                "generation_settings": {"temperature": "default"},
                "notes": "Synthetic test outputs; no model was called.",
            }
        ),
        encoding="utf-8",
    )
    output_path = run_dir / "outputs.jsonl"
    imported = _run(
        "import-antigravity",
        str(run_dir),
        str(response_dir),
        "--metadata",
        str(metadata_path),
        "--output",
        str(output_path),
    )
    assert imported.returncode == 0, imported.stderr
    assert "imported 24 Antigravity responses" in imported.stdout
    report_path = run_dir / "report.json"
    scored = _run(
        "score",
        str(run_dir),
        str(output_path),
        "--report",
        str(report_path),
    )
    assert scored.returncode == 0, scored.stderr
    report = json.loads(report_path.read_text())
    assert report["aggregates"]["skill"]["passed"] == 12
    assert report["aggregates"]["baseline"]["passed"] == 0
    assert report["aggregates"]["baseline"]["rule_counts"]["GTTA004"] == 12
    assert report["scope"] == "deterministic-method-contract-only"
    assert report["seed"] == 7
    assert report["skill_sha256"] == mapping["skill_sha256"]
    assert report["run_metadata"]["runner"] == "Antigravity"
    assert report["run_metadata"]["sample_count"] == 24


def test_antigravity_import_rejects_incomplete_response_set(tmp_path):
    run_dir = tmp_path / "run"
    assert _run("prepare", str(run_dir)).returncode == 0
    metadata_path = run_dir / "metadata.json"
    metadata_path.write_text(
        json.dumps(
            {
                "runner": "Antigravity",
                "app_version": "2.11.0",
                "model": "test-model",
                "generation_settings": {},
                "notes": "",
            }
        ),
        encoding="utf-8",
    )
    output_path = run_dir / "outputs.jsonl"
    result = _run(
        "import-antigravity",
        str(run_dir),
        str(run_dir / "antigravity-responses"),
        "--metadata",
        str(metadata_path),
        "--output",
        str(output_path),
    )
    assert result.returncode == 2
    assert "missing=24" in result.stderr
    assert not output_path.exists()


def test_antigravity_import_does_not_overwrite_recorded_metadata_path(tmp_path):
    run_dir = tmp_path / "run"
    assert _run("prepare", str(run_dir)).returncode == 0
    result = _run(
        "import-antigravity",
        str(run_dir),
        str(run_dir / "antigravity-responses"),
        "--metadata",
        str(run_dir / "run-metadata.template.json"),
        "--output",
        str(run_dir / "run-metadata.json"),
    )
    assert result.returncode == 2
    assert "must not overwrite run-metadata.json" in result.stderr
    assert not (run_dir / "run-metadata.json").exists()


def test_published_antigravity_run_reproduces(tmp_path):
    metadata = json.loads((PUBLISHED_RUN / "run-metadata.json").read_text())
    requests_hash = hashlib.sha256(
        (PUBLISHED_RUN / "requests.jsonl").read_bytes()
    ).hexdigest()
    outputs_hash = hashlib.sha256(
        (PUBLISHED_RUN / "outputs.jsonl").read_bytes()
    ).hexdigest()
    mapping = json.loads((PUBLISHED_RUN / "private-mapping.json").read_text())
    skill_hash = hashlib.sha256((ROOT / "SKILL.md").read_bytes()).hexdigest()
    assert requests_hash == metadata["requests_sha256"]
    assert outputs_hash == metadata["outputs_sha256"]
    assert skill_hash == mapping["skill_sha256"]

    recomputed_path = tmp_path / "report.json"
    result = _run(
        "score",
        str(PUBLISHED_RUN),
        str(PUBLISHED_RUN / "outputs.jsonl"),
        "--report",
        str(recomputed_path),
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(recomputed_path.read_text()) == json.loads(
        (PUBLISHED_RUN / "report.json").read_text()
    )
