import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "agent_eval.py"


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

    output_path = run_dir / "outputs.jsonl"
    output_path.write_text(
        "\n".join(json.dumps(row) for row in outputs) + "\n",
        encoding="utf-8",
    )
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
