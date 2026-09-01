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
REPLICATION_RUN = (
    ROOT
    / "evals"
    / "agent-eval"
    / "runs"
    / "2026-08-30-antigravity-gemini-3.7-flash-high-seed-20260831"
)
CROSS_MODEL_RUN = (
    ROOT
    / "evals"
    / "agent-eval"
    / "runs"
    / "2026-08-31-antigravity-claude-opus-4.6-thinking-seed-20260901"
)
CLAUDE_REPLICATION_RUN = (
    ROOT
    / "evals"
    / "agent-eval"
    / "runs"
    / "2026-09-01-antigravity-claude-opus-4.6-thinking-seed-20260902"
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
            if sample["case_id"] == "ai-governance-cloud":
                output += "\n" + "\n".join(
                    "The regulator is likely to delay implementation in "
                    f"scenario {index}."
                    for index in range(26)
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
    assert report["findings_truncated"] is True
    assert report["finding_limits"] == {"GTTA010": 25}
    assert report["aggregates"]["skill"]["truncated_samples"] == 1
    assert report["aggregates"]["skill"]["truncated_rule_counts"] == {
        "GTTA010": 1
    }
    truncated_sample = next(
        row for row in report["samples"] if row["findings_truncated"]
    )
    assert truncated_sample["case_id"] == "ai-governance-cloud"
    assert truncated_sample["truncated_rule_ids"] == ["GTTA010"]


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


def _write_outputs(
    run_dir: Path,
    output_path: Path,
    values: dict[tuple[str, str], str],
):
    mapping = json.loads((run_dir / "private-mapping.json").read_text())
    rows = [
        {
            "sample_id": sample["sample_id"],
            "output": values[(sample["case_id"], sample["arm"])],
        }
        for sample in mapping["samples"]
    ]
    output_path.write_text(
        "\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8"
    )


def test_freshness_gate_rejects_exact_and_cosmetic_reuse(tmp_path):
    first = tmp_path / "first"
    candidate = tmp_path / "candidate"
    assert _run("prepare", str(first), "--seed", "1").returncode == 0
    assert _run("prepare", str(candidate), "--seed", "2").returncode == 0
    first_mapping = json.loads((first / "private-mapping.json").read_text())
    keys = {(row["case_id"], row["arm"]) for row in first_mapping["samples"]}
    original = {
        key: "\n".join(f"Original line {index} for {key}." for index in range(12))
        for key in keys
    }
    changed = {
        key: "\n".join("z" * (80 + index) for index in range(12))
        for key in keys
    }
    exact_key = ("ai-governance-cloud", "baseline")
    near_key = ("cbam-enforcement", "skill")
    changed[exact_key] = original[exact_key]
    changed[near_key] = original[near_key].replace("Original line 0", "Reworded line 0")
    _write_outputs(first, first / "outputs.jsonl", original)
    _write_outputs(candidate, candidate / "outputs.jsonl", changed)

    report_path = tmp_path / "freshness.json"
    result = _run(
        "verify-freshness",
        str(candidate),
        str(candidate / "outputs.jsonl"),
        "--against",
        str(first),
        str(first / "outputs.jsonl"),
        "--report",
        str(report_path),
    )
    assert result.returncode == 2
    report = json.loads(report_path.read_text())
    assert report["passed"] is False
    comparison = report["comparisons"][0]
    assert comparison["exact_duplicates"] == [
        {"case_id": exact_key[0], "arm": exact_key[1]}
    ]
    assert [
        (row["case_id"], row["arm"]) for row in comparison["near_duplicates"]
    ] == [near_key]
    assert comparison["max_observed"]["sequence_similarity"]["value"] == 1.0
    assert comparison["max_observed"]["shared_line_ratio"]["value"] == 1.0


def test_freshness_gate_accepts_materially_distinct_outputs(tmp_path):
    first = tmp_path / "first"
    candidate = tmp_path / "candidate"
    assert _run("prepare", str(first), "--seed", "1").returncode == 0
    assert _run("prepare", str(candidate), "--seed", "2").returncode == 0
    mapping = json.loads((first / "private-mapping.json").read_text())
    keys = {(row["case_id"], row["arm"]) for row in mapping["samples"]}
    _write_outputs(
        first,
        first / "outputs.jsonl",
        {key: f"Alpha evidence and scenario for {key}." for key in keys},
    )
    _write_outputs(
        candidate,
        candidate / "outputs.jsonl",
        {key: f"Completely separate decision memo about {key}." for key in keys},
    )
    result = _run(
        "verify-freshness",
        str(candidate),
        str(candidate / "outputs.jsonl"),
        "--against",
        str(first),
        str(first / "outputs.jsonl"),
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["passed"] is True
    assert report["comparisons"][0]["max_observed"]["sequence_similarity"][
        "value"
    ] < 0.90


def test_published_antigravity_run_reproduces(tmp_path):
    metadata = json.loads((PUBLISHED_RUN / "run-metadata.json").read_text())
    requests_hash = hashlib.sha256(
        (PUBLISHED_RUN / "requests.jsonl").read_bytes()
    ).hexdigest()
    outputs_hash = hashlib.sha256(
        (PUBLISHED_RUN / "outputs.jsonl").read_bytes()
    ).hexdigest()
    mapping = json.loads((PUBLISHED_RUN / "private-mapping.json").read_text())
    requests = [
        json.loads(line)
        for line in (PUBLISHED_RUN / "requests.jsonl").read_text().splitlines()
    ]
    embedded_skill_hashes = set()
    for request in requests:
        system = request["messages"][0]["content"]
        if "<gtta-skill>" not in system:
            continue
        skill_text = system.split("<gtta-skill>\n", 1)[1].rsplit(
            "\n</gtta-skill>", 1
        )[0]
        embedded_skill_hashes.add(hashlib.sha256(skill_text.encode()).hexdigest())
    assert requests_hash == metadata["requests_sha256"]
    assert outputs_hash == metadata["outputs_sha256"]
    assert embedded_skill_hashes == {mapping["skill_sha256"]}

    original_report = json.loads((PUBLISHED_RUN / "report.json").read_text())
    assert original_report["ruleset_version"] == "gtta-method-contract@1.1.0"
    assert original_report["run_metadata"] == metadata
    assert original_report["skill_sha256"] == mapping["skill_sha256"]
    for arm in ("baseline", "skill"):
        details = [row for row in original_report["samples"] if row["arm"] == arm]
        aggregate = original_report["aggregates"][arm]
        assert aggregate["samples"] == len(details)
        assert aggregate["passed"] == sum(row["passed"] for row in details)
        assert aggregate["error_findings"] == sum(
            finding["severity"] == "error"
            for row in details
            for finding in row["findings"]
        )
        assert aggregate["warning_findings"] == sum(
            finding["severity"] == "warning"
            for row in details
            for finding in row["findings"]
        )

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
        (PUBLISHED_RUN / "rescore-gtta-method-contract-1.2.3.json").read_text()
    )


def test_published_antigravity_replication_reproduces(tmp_path):
    metadata = json.loads((REPLICATION_RUN / "run-metadata.json").read_text())
    mapping = json.loads((REPLICATION_RUN / "private-mapping.json").read_text())
    report = json.loads((REPLICATION_RUN / "report.json").read_text())
    requests = [
        json.loads(line)
        for line in (REPLICATION_RUN / "requests.jsonl").read_text().splitlines()
    ]
    embedded_skill_hashes = set()
    for request in requests:
        system = request["messages"][0]["content"]
        if "<gtta-skill>" not in system:
            continue
        skill_text = system.split("<gtta-skill>\n", 1)[1].rsplit(
            "\n</gtta-skill>", 1
        )[0]
        embedded_skill_hashes.add(hashlib.sha256(skill_text.encode()).hexdigest())

    assert hashlib.sha256(
        (REPLICATION_RUN / "requests.jsonl").read_bytes()
    ).hexdigest() == metadata["requests_sha256"]
    assert hashlib.sha256(
        (REPLICATION_RUN / "outputs.jsonl").read_bytes()
    ).hexdigest() == metadata["outputs_sha256"]
    assert metadata["sample_count"] == 24
    assert mapping["seed"] == report["seed"] == 20260831
    assert embedded_skill_hashes == {mapping["skill_sha256"]}
    assert report["skill_sha256"] == mapping["skill_sha256"]
    assert report["ruleset_version"] == "gtta-method-contract@1.2.0"
    assert report["aggregates"]["baseline"]["passed"] == 0
    assert report["aggregates"]["skill"]["passed"] == 12
    assert report["aggregates"]["skill"]["warning_findings"] == 13

    recomputed_score = tmp_path / "replication-score.json"
    score = _run(
        "score",
        str(REPLICATION_RUN),
        str(REPLICATION_RUN / "outputs.jsonl"),
        "--report",
        str(recomputed_score),
    )
    assert score.returncode == 0, score.stderr
    current_rescore = json.loads(
        (REPLICATION_RUN / "rescore-gtta-method-contract-1.2.3.json").read_text()
    )
    assert json.loads(recomputed_score.read_text()) == current_rescore
    assert current_rescore["ruleset_version"] == "gtta-method-contract@1.2.3"
    assert current_rescore["aggregates"]["skill"]["warning_findings"] == 12
    assert current_rescore["findings_truncated"] is False

    recomputed_freshness = tmp_path / "replication-freshness.json"
    replication_relative = REPLICATION_RUN.relative_to(ROOT)
    published_relative = PUBLISHED_RUN.relative_to(ROOT)
    freshness = _run(
        "verify-freshness",
        str(replication_relative),
        str(replication_relative / "outputs.jsonl"),
        "--against",
        str(published_relative),
        str(published_relative / "outputs.jsonl"),
        "--report",
        str(recomputed_freshness),
    )
    assert freshness.returncode == 0, freshness.stderr
    published_freshness = json.loads(
        (REPLICATION_RUN / "freshness-report.json").read_text()
    )
    assert json.loads(recomputed_freshness.read_text()) == published_freshness
    assert published_freshness["passed"] is True


def test_published_cross_model_run_reproduces(tmp_path):
    metadata = json.loads((CROSS_MODEL_RUN / "run-metadata.json").read_text())
    mapping = json.loads((CROSS_MODEL_RUN / "private-mapping.json").read_text())
    report = json.loads((CROSS_MODEL_RUN / "report.json").read_text())
    requests = [
        json.loads(line)
        for line in (CROSS_MODEL_RUN / "requests.jsonl").read_text().splitlines()
    ]
    embedded_skill_hashes = set()
    for request in requests:
        system = request["messages"][0]["content"]
        if "<gtta-skill>" not in system:
            continue
        skill_text = system.split("<gtta-skill>\n", 1)[1].rsplit(
            "\n</gtta-skill>", 1
        )[0]
        embedded_skill_hashes.add(hashlib.sha256(skill_text.encode()).hexdigest())

    assert hashlib.sha256(
        (CROSS_MODEL_RUN / "requests.jsonl").read_bytes()
    ).hexdigest() == metadata["requests_sha256"]
    assert hashlib.sha256(
        (CROSS_MODEL_RUN / "outputs.jsonl").read_bytes()
    ).hexdigest() == metadata["outputs_sha256"]
    assert metadata["runner"] == "Antigravity"
    assert metadata["app_version"] == "2.11.0"
    assert metadata["model"] == "Claude Opus 4.6 (Thinking)"
    assert metadata["generation_settings"] == {}
    assert metadata["sample_count"] == 24
    assert mapping["seed"] == report["seed"] == 20260901
    assert embedded_skill_hashes == {mapping["skill_sha256"]}
    assert report["skill_sha256"] == mapping["skill_sha256"]
    assert report["ruleset_version"] == "gtta-method-contract@1.2.1"
    assert report["aggregates"]["baseline"]["passed"] == 0
    assert report["aggregates"]["skill"]["passed"] == 12
    assert report["aggregates"]["skill"]["warning_findings"] == 181

    recomputed_score = tmp_path / "cross-model-score.json"
    score = _run(
        "score",
        str(CROSS_MODEL_RUN),
        str(CROSS_MODEL_RUN / "outputs.jsonl"),
        "--report",
        str(recomputed_score),
    )
    assert score.returncode == 0, score.stderr
    current_rescore = json.loads(
        (CROSS_MODEL_RUN / "rescore-gtta-method-contract-1.2.3.json").read_text()
    )
    assert json.loads(recomputed_score.read_text()) == current_rescore
    assert current_rescore["ruleset_version"] == "gtta-method-contract@1.2.3"
    assert current_rescore["aggregates"]["baseline"]["warning_findings"] == 360
    assert current_rescore["aggregates"]["skill"]["warning_findings"] == 170
    assert current_rescore["aggregates"]["skill"]["rule_counts"] == {
        "GTTA008": 2,
        "GTTA010": 168,
    }
    assert current_rescore["findings_truncated"] is True
    assert current_rescore["aggregates"]["baseline"]["truncated_samples"] == 12
    assert current_rescore["aggregates"]["skill"]["truncated_samples"] == 2

    recomputed_freshness = tmp_path / "cross-model-freshness.json"
    cross_model_relative = CROSS_MODEL_RUN.relative_to(ROOT)
    published_relative = PUBLISHED_RUN.relative_to(ROOT)
    replication_relative = REPLICATION_RUN.relative_to(ROOT)
    freshness = _run(
        "verify-freshness",
        str(cross_model_relative),
        str(cross_model_relative / "outputs.jsonl"),
        "--against",
        str(published_relative),
        str(published_relative / "outputs.jsonl"),
        "--against",
        str(replication_relative),
        str(replication_relative / "outputs.jsonl"),
        "--report",
        str(recomputed_freshness),
    )
    assert freshness.returncode == 0, freshness.stderr
    published_freshness = json.loads(
        (CROSS_MODEL_RUN / "freshness-report.json").read_text()
    )
    assert json.loads(recomputed_freshness.read_text()) == published_freshness
    assert published_freshness["passed"] is True
    assert all(
        not comparison["exact_duplicates"]
        and not comparison["near_duplicates"]
        for comparison in published_freshness["comparisons"]
    )


def test_published_claude_replication_reproduces(tmp_path):
    metadata = json.loads(
        (CLAUDE_REPLICATION_RUN / "run-metadata.json").read_text()
    )
    mapping = json.loads(
        (CLAUDE_REPLICATION_RUN / "private-mapping.json").read_text()
    )
    report = json.loads((CLAUDE_REPLICATION_RUN / "report.json").read_text())
    requests = [
        json.loads(line)
        for line in (CLAUDE_REPLICATION_RUN / "requests.jsonl")
        .read_text()
        .splitlines()
    ]
    embedded_skill_hashes = set()
    for request in requests:
        system = request["messages"][0]["content"]
        if "<gtta-skill>" not in system:
            continue
        skill_text = system.split("<gtta-skill>\n", 1)[1].rsplit(
            "\n</gtta-skill>", 1
        )[0]
        embedded_skill_hashes.add(hashlib.sha256(skill_text.encode()).hexdigest())

    assert hashlib.sha256(
        (CLAUDE_REPLICATION_RUN / "requests.jsonl").read_bytes()
    ).hexdigest() == metadata["requests_sha256"]
    assert hashlib.sha256(
        (CLAUDE_REPLICATION_RUN / "outputs.jsonl").read_bytes()
    ).hexdigest() == metadata["outputs_sha256"]
    assert metadata["runner"] == "Antigravity"
    assert metadata["app_version"] == "2.11.0"
    assert metadata["model"] == "Claude Opus 4.6 (Thinking)"
    assert metadata["generation_settings"] == {}
    assert metadata["sample_count"] == 24
    assert mapping["seed"] == report["seed"] == 20260902
    assert embedded_skill_hashes == {mapping["skill_sha256"]}
    assert report["skill_sha256"] == mapping["skill_sha256"]
    assert report["ruleset_version"] == "gtta-method-contract@1.2.2"
    assert report["aggregates"]["baseline"]["passed"] == 0
    assert report["aggregates"]["baseline"]["warning_findings"] == 359
    assert report["aggregates"]["skill"]["passed"] == 12
    assert report["aggregates"]["skill"]["warning_findings"] == 111
    assert report["aggregates"]["skill"]["rule_counts"] == {
        "GTTA008": 1,
        "GTTA010": 110,
    }

    recomputed_score = tmp_path / "claude-replication-score.json"
    score = _run(
        "score",
        str(CLAUDE_REPLICATION_RUN),
        str(CLAUDE_REPLICATION_RUN / "outputs.jsonl"),
        "--report",
        str(recomputed_score),
    )
    assert score.returncode == 0, score.stderr
    current_rescore = json.loads(
        (
            CLAUDE_REPLICATION_RUN
            / "rescore-gtta-method-contract-1.2.3.json"
        ).read_text()
    )
    assert json.loads(recomputed_score.read_text()) == current_rescore
    assert current_rescore["ruleset_version"] == "gtta-method-contract@1.2.3"
    assert current_rescore["aggregates"]["skill"]["warning_findings"] == 111
    assert current_rescore["aggregates"]["baseline"]["truncated_samples"] == 11
    assert current_rescore["aggregates"]["skill"]["truncated_samples"] == 3
    assert current_rescore["aggregates"]["skill"]["truncated_rule_counts"] == {
        "GTTA010": 3
    }

    recomputed_freshness = tmp_path / "claude-replication-freshness.json"
    candidate_relative = CLAUDE_REPLICATION_RUN.relative_to(ROOT)
    published_relative = PUBLISHED_RUN.relative_to(ROOT)
    replication_relative = REPLICATION_RUN.relative_to(ROOT)
    cross_model_relative = CROSS_MODEL_RUN.relative_to(ROOT)
    freshness = _run(
        "verify-freshness",
        str(candidate_relative),
        str(candidate_relative / "outputs.jsonl"),
        "--against",
        str(published_relative),
        str(published_relative / "outputs.jsonl"),
        "--against",
        str(replication_relative),
        str(replication_relative / "outputs.jsonl"),
        "--against",
        str(cross_model_relative),
        str(cross_model_relative / "outputs.jsonl"),
        "--report",
        str(recomputed_freshness),
    )
    assert freshness.returncode == 0, freshness.stderr
    published_freshness = json.loads(
        (CLAUDE_REPLICATION_RUN / "freshness-report.json").read_text()
    )
    assert json.loads(recomputed_freshness.read_text()) == published_freshness
    assert published_freshness["passed"] is True
    assert len(published_freshness["comparisons"]) == 3
    assert all(
        not comparison["exact_duplicates"]
        and not comparison["near_duplicates"]
        for comparison in published_freshness["comparisons"]
    )
