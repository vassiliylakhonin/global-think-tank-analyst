"""SARIF 2.1.0 projection for method-contract findings."""

from __future__ import annotations

from typing import Any

from .discipline import ContractReport

_RULES = {
    "GTTA001": "Memo text is present",
    "GTTA002": "Evidence mode is declared",
    "GTTA003": "Evidence mode is canonical",
    "GTTA004": "Axis A provenance is present",
    "GTTA005": "Inference or judgment is explicit",
    "GTTA006": "Confidence is explicit",
    "GTTA007": "Change conditions are stated",
    "GTTA008": "Mode output markers are present",
    "GTTA009": "Recommendations use observable triggers",
    "GTTA010": "Likely claims carry inline provenance",
}


def render_contract_sarif(
    report: ContractReport, *, artifact_uri: str
) -> dict[str, Any]:
    """Render a stable SARIF result without changing contract semantics."""

    results: list[dict[str, Any]] = []
    for finding in report.findings:
        result: dict[str, Any] = {
            "ruleId": finding.rule_id,
            "level": finding.severity.value,
            "message": {"text": finding.message},
        }
        if finding.line is not None:
            result["locations"] = [
                {
                    "physicalLocation": {
                        "artifactLocation": {"uri": artifact_uri},
                        "region": {"startLine": finding.line},
                    }
                }
            ]
        results.append(result)

    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "gtta-method-contract",
                        "semanticVersion": report.ruleset_version.rsplit("@", 1)[-1],
                        "informationUri": (
                            "https://github.com/vassiliylakhonin/"
                            "global-think-tank-analyst"
                        ),
                        "rules": [
                            {
                                "id": rule_id,
                                "shortDescription": {"text": description},
                            }
                            for rule_id, description in _RULES.items()
                        ],
                    }
                },
                "results": results,
                "properties": {
                    "scope": "method-contract-only",
                    "findingsTruncated": bool(report.truncated_rule_ids),
                    "truncatedRuleIds": list(report.truncated_rule_ids),
                },
            }
        ],
    }
