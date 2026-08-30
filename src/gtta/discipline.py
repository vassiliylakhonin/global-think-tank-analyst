"""Deterministic preflight for the Policy Risk Memo Architect contract.

This module checks observable method structure. It deliberately does not check
whether claims are true or supported by sources; that belongs to the companion
Agenda Intelligence MD evidence-packet seam and ultimately to human review.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


RULESET_VERSION = "gtta-method-contract@0.1.0"
SUPPORTED_EVIDENCE_MODES = (
    "live-source-backed",
    "user-provided sources",
    "illustrative source packet",
    "reasoning-only",
)
AXIS_A_TAGS = (
    "[primary]",
    "[secondary]",
    "[user-provided]",
    "[inference]",
    "[analyst-judgment]",
)


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: Severity
    message: str
    line: Optional[int] = None

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "rule_id": self.rule_id,
            "severity": self.severity.value,
            "message": self.message,
        }
        if self.line is not None:
            result["line"] = self.line
        return result


@dataclass(frozen=True)
class ContractReport:
    ruleset_version: str
    mode: Optional[str]
    evidence_mode: Optional[str]
    findings: tuple[Finding, ...]

    @property
    def passed(self) -> bool:
        return not any(item.severity is Severity.ERROR for item in self.findings)

    def to_dict(self) -> dict[str, object]:
        return {
            "ruleset_version": self.ruleset_version,
            "scope": "method-contract-only",
            "passed": self.passed,
            "mode": self.mode,
            "evidence_mode": self.evidence_mode,
            "findings": [item.to_dict() for item in self.findings],
            "limitations": (
                "No factuality, URL availability, or claim/source support "
                "verification was performed."
            ),
        }

    def render_text(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        lines = [f"GTTA method-contract preflight: {status} ({self.ruleset_version})"]
        if not self.findings:
            lines.append("No deterministic method-contract findings.")
        for item in self.findings:
            location = f" line {item.line}" if item.line is not None else ""
            lines.append(
                f"- {item.severity.value.upper()} {item.rule_id}{location}: "
                f"{item.message}"
            )
        lines.append(
            "Limit: no factuality or claim/source support verification was performed."
        )
        return "\n".join(lines)


_MODE_REQUIREMENTS = {
    "A": ("bottom line", "main risks", "what to watch"),
    "B": ("executive takeaway", "decision context", "actors", "options"),
    "C": ("baseline", "scenarios", "triggers", "indicators"),
    "D": ("target claim", "alternative explanations", "revised judgment"),
    "E": ("executive takeaway", "options", "watchlist", "questions for owners"),
    "F": ("coaching",),
    "G": ("hypotheses", "evidence matrix", "sensitivity", "bounded judgment"),
}


def _line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def _extract_evidence_mode(text: str) -> tuple[Optional[str], Optional[int]]:
    for line_number, line in enumerate(text.splitlines(), start=1):
        plain = line.replace("**", "").replace("`", "").lstrip("> ").strip()
        match = re.search(r"evidence mode\s*:\s*(.+)", plain, re.IGNORECASE)
        if not match:
            continue
        declared = match.group(1).strip().lower()
        for mode in SUPPORTED_EVIDENCE_MODES:
            if declared.startswith(mode):
                return mode, line_number
        return declared.rstrip("."), line_number
    return None, None


def check_contract(text: str, mode: Optional[str] = None) -> ContractReport:
    """Check deterministic, observable parts of the analytical contract.

    Errors are limited to declarations the method requires unambiguously.
    Warnings cover useful mode-shape and language heuristics that may require
    human interpretation.
    """
    normalized_mode = mode.strip().upper().removeprefix("MODE ") if mode else None
    if normalized_mode is not None and normalized_mode not in _MODE_REQUIREMENTS:
        raise ValueError("Memo mode must be one of A, B, C, D, E, F, or G.")

    findings: list[Finding] = []
    evidence_mode, evidence_line = _extract_evidence_mode(text)

    if not text.strip():
        findings.append(
            Finding("GTTA001", Severity.ERROR, "Memo text is empty.")
        )
    if evidence_mode is None:
        findings.append(
            Finding(
                "GTTA002",
                Severity.ERROR,
                "Declare one canonical evidence mode.",
            )
        )
    elif evidence_mode not in SUPPORTED_EVIDENCE_MODES:
        findings.append(
            Finding(
                "GTTA003",
                Severity.ERROR,
                f"Unsupported evidence mode {evidence_mode!r}.",
                evidence_line,
            )
        )

    if normalized_mode != "F" and not any(tag in text for tag in AXIS_A_TAGS):
        findings.append(
            Finding(
                "GTTA004",
                Severity.ERROR,
                "No Axis A provenance tag was found.",
            )
        )

    if normalized_mode != "F" and not any(
        tag in text for tag in ("[inference]", "[analyst-judgment]")
    ):
        findings.append(
            Finding(
                "GTTA005",
                Severity.WARNING,
                "No explicit inference or analyst-judgment tag was found.",
            )
        )

    confidence = re.search(
        r"(?im)(?:confidence[^\n]{0,80}\b(?:low|moderate|high)\b|"
        r"\b(?:low|moderate|high)\s+confidence\b)",
        text,
    )
    if normalized_mode != "F" and confidence is None:
        findings.append(
            Finding(
                "GTTA006",
                Severity.WARNING,
                "No explicit Low, Moderate, or High confidence statement was found.",
            )
        )

    lower_text = text.lower()
    if normalized_mode in {"B", "E", "G"} and not any(
        phrase in lower_text
        for phrase in ("what would change", "what could change", "change this judgment")
    ):
        findings.append(
            Finding(
                "GTTA007",
                Severity.WARNING,
                "Deeper memo lacks an explicit 'what would change the judgment' section.",
            )
        )

    if normalized_mode is not None:
        for phrase in _MODE_REQUIREMENTS[normalized_mode]:
            if phrase not in lower_text:
                findings.append(
                    Finding(
                        "GTTA008",
                        Severity.WARNING,
                        f"Mode {normalized_mode} output marker {phrase!r} was not found.",
                    )
                )

    for phrase in ("monitor the situation", "remain agile", "stay flexible"):
        position = lower_text.find(phrase)
        if position != -1:
            findings.append(
                Finding(
                    "GTTA009",
                    Severity.WARNING,
                    f"Generic recommendation {phrase!r} needs an observable trigger.",
                    _line_number(text, position),
                )
            )

    return ContractReport(
        ruleset_version=RULESET_VERSION,
        mode=normalized_mode,
        evidence_mode=evidence_mode,
        findings=tuple(findings),
    )
