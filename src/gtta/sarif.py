"""SARIF 2.1.0 projections for GTTA's deterministic checks."""

from __future__ import annotations

import re
from typing import Any

from .discipline import ContractReport
from .verification import MemoVerificationReport

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

_VERIFICATION_RULES: dict[str, tuple[str, str]] = {
    "GTTAV001": (
        "Risk-sensitive claim declares verification work or dated primary basis",
        "warning",
    ),
    "GTTAV002": ("Agenda rejected the projected evidence-packet contract", "error"),
    "AGENDA001": ("Claim names at least one source", "error"),
    "AGENDA002": ("Referenced source is present in the evidence packet", "error"),
    "AGENDA003": ("Quoted source is present in the evidence packet", "error"),
    "AGENDA004": ("Quoted source is declared by the claim", "error"),
    "AGENDA005": ("Declared quote occurs in its source", "error"),
    "AGENDA006": ("Claim and source do not conflict on polarity", "warning"),
    "AGENDA007": ("Claim has adequate lexical support", "warning"),
    "AGENDA008": ("Claim has lexical support", "warning"),
    "AGENDA009": ("Claim numbers occur in its referenced sources", "warning"),
    "AGENDA999": ("Agenda evidence-packet issue", "warning"),
}

_AGENDA_ISSUE_RULES = {
    "no_source_reference": "AGENDA001",
    "lexical_support_polarity_mismatch": "AGENDA006",
    "lexical_support_weak": "AGENDA007",
    "lexical_support_unsupported": "AGENDA008",
    "unmatched_numbers": "AGENDA009",
}

_AGENDA_PREFIX_RULES = (
    ("missing_source:", "AGENDA002"),
    ("quote_source_missing:", "AGENDA003"),
    ("quote_source_not_declared:", "AGENDA004"),
    ("quote_absent:", "AGENDA005"),
)

_CLAIM_ID_RE = re.compile(r'"claim_id"\s*:\s*"(?P<claim_id>[A-Za-z][A-Za-z0-9._-]{0,63})"')


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


def _claim_line_map(artifact_text: str) -> dict[str, int]:
    lines: dict[str, int] = {}
    for line_number, line in enumerate(artifact_text.splitlines(), start=1):
        for match in _CLAIM_ID_RE.finditer(line):
            lines.setdefault(match.group("claim_id"), line_number)
    return lines


def _agenda_rule_id(issue: str) -> str:
    if issue in _AGENDA_ISSUE_RULES:
        return _AGENDA_ISSUE_RULES[issue]
    for prefix, rule_id in _AGENDA_PREFIX_RULES:
        if issue.startswith(prefix):
            return rule_id
    return "AGENDA999"


def _location(artifact_uri: str, line: int | None = None) -> list[dict[str, Any]]:
    physical: dict[str, Any] = {"artifactLocation": {"uri": artifact_uri}}
    if line is not None:
        physical["region"] = {"startLine": line}
    return [{"physicalLocation": physical}]


def render_verification_sarif(
    report: MemoVerificationReport,
    *,
    artifact_uri: str,
    artifact_text: str,
) -> dict[str, Any]:
    """Render GTTA and Agenda verification findings through one stable adapter."""

    claim_lines = _claim_line_map(artifact_text)
    results: list[dict[str, Any]] = []
    for finding in report.findings:
        results.append(
            {
                "ruleId": finding.rule_id,
                "level": "warning",
                "message": {"text": finding.message},
                "locations": _location(
                    artifact_uri, claim_lines.get(finding.claim_id)
                ),
                "properties": {
                    "claimId": finding.claim_id,
                    "source": "gtta-preflight",
                },
            }
        )

    for error in report.agenda_result.get("errors", []) or []:
        results.append(
            {
                "ruleId": "GTTAV002",
                "level": "error",
                "message": {"text": str(error)},
                "locations": _location(artifact_uri, 1),
                "properties": {"source": "agenda-contract"},
            }
        )

    response = report.agenda_result.get("response") or {}
    claim_results = response.get("claims", []) or []
    for claim_result in claim_results:
        if not isinstance(claim_result, dict):
            continue
        claim_id = str(claim_result.get("claim_id") or "unknown")
        packet_status = str(claim_result.get("packet_status") or "unknown")
        for issue_value in claim_result.get("issues", []) or []:
            issue = str(issue_value)
            rule_id = _agenda_rule_id(issue)
            _, level = _VERIFICATION_RULES[rule_id]
            results.append(
                {
                    "ruleId": rule_id,
                    "level": level,
                    "message": {
                        "text": f"Claim {claim_id}: Agenda reported {issue}."
                    },
                    "locations": _location(
                        artifact_uri, claim_lines.get(claim_id)
                    ),
                    "properties": {
                        "claimId": claim_id,
                        "issueCode": issue,
                        "packetStatus": packet_status,
                        "source": "agenda-evidence-packet",
                    },
                }
            )

    factuality_status = response.get("factuality_status") or "not_assessed"
    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "gtta-memo-verification",
                        "semanticVersion": "1.0.0",
                        "informationUri": (
                            "https://github.com/vassiliylakhonin/"
                            "global-think-tank-analyst"
                        ),
                        "rules": [
                            {
                                "id": rule_id,
                                "shortDescription": {"text": description},
                                "defaultConfiguration": {"level": level},
                            }
                            for rule_id, (description, level) in _VERIFICATION_RULES.items()
                        ],
                    }
                },
                "results": results,
                "properties": {
                    "scope": "memo-artifact-to-evidence-packet-preflight",
                    "strict": report.strict,
                    "passed": report.passed,
                    "packetStatus": report.packet_status,
                    "factualityStatus": factuality_status,
                    "humanReviewRequired": True,
                },
            }
        ],
    }
