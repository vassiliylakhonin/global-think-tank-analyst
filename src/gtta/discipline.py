"""Deterministic preflight for the Policy Risk Memo Architect contract.

This module checks observable method structure. It deliberately does not check
whether claims are true or supported by sources; that belongs to the companion
Agenda Intelligence MD evidence-packet seam and ultimately to human review.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


RULESET_VERSION = "gtta-method-contract@1.2.1"
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
    "A": (
        ("bottom line",),
        ("main risks",),
        ("what to watch", "indicators"),
    ),
    "B": (
        ("executive takeaway",),
        ("decision context",),
        ("actors", "actor incentives"),
        ("options",),
    ),
    "C": (
        ("baseline", "baseline outlook"),
        ("scenarios", "scenario planning", "scenario pathways"),
        ("triggers", "decision triggers"),
        ("indicators", "what to watch"),
    ),
    "D": (
        ("target claim",),
        ("alternative explanations",),
        ("revised judgment",),
    ),
    "E": (
        ("executive takeaway",),
        ("options", "decision matrix"),
        ("watchlist", "leading indicators"),
        (
            "questions for owners",
            "questions for decision owners",
            "questions for management & decision owners",
        ),
    ),
    "F": (("coaching", "coaching questions"),),
    "G": (
        ("hypotheses",),
        ("evidence matrix", "evidence evaluation matrix"),
        ("sensitivity",),
        ("bounded judgment",),
    ),
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


_NON_CLAIM_HEADINGS = {
    "confidence",
    "key unknowns",
    "limitations",
    "sources",
}
_METADATA_PREFIXES = (
    "to:",
    "from:",
    "date:",
    "subject:",
    "prepared for:",
    "question:",
    "decision:",
    "change condition:",
    "audience:",
    "time horizon:",
    "evidence mode:",
    "depth:",
    "retrieval date:",
    "confidence:",
)
_TABLE_LABEL_WORDS = {
    "actor",
    "actors",
    "hypothesis",
    "hypotheses",
    "indicator",
    "indicators",
    "option",
    "options",
    "owner",
    "owners",
    "risk",
    "risks",
    "scenario",
    "scenarios",
    "stakeholder",
    "stakeholders",
}
_TABLE_SEPARATOR = re.compile(r"\|?(?:\s*:?-+:?\s*\|)+\s*")
_BOLD_SECTION_LABEL = re.compile(r"^(?:\d+\.\s*)?\*\*[^*]+:\*\*\s*$")


def _looks_like_material_claim(fragment: str) -> bool:
    plain = re.sub(r"[`*_>#-]", " ", fragment).strip()
    lowered = plain.lower()
    if not plain or plain.endswith("?") or lowered.startswith(_METADATA_PREFIXES):
        return False
    if plain.startswith("[") and plain.endswith("]"):
        return False
    words = re.findall(r"\b[^\W\d_][\w'-]*\b", plain, flags=re.UNICODE)
    return len(plain) >= 35 and len(words) >= 5


def _table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _table_layout(lines: list[str]) -> tuple[set[int], dict[int, set[int]]]:
    """Locate Markdown headers and identifier columns for each table row."""
    header_lines: set[int] = set()
    label_columns_by_row: dict[int, set[int]] = {}
    index = 0
    while index + 1 < len(lines):
        if "|" not in lines[index] or not _TABLE_SEPARATOR.fullmatch(
            lines[index + 1].strip()
        ):
            index += 1
            continue

        header_lines.update({index, index + 1})
        label_columns: set[int] = set()
        for column, cell in enumerate(_table_cells(lines[index])):
            plain = re.sub(r"[`*_]", "", cell).strip().lower()
            words = set(re.findall(r"[a-z]+", plain))
            if column == 0 and words & _TABLE_LABEL_WORDS:
                label_columns.add(column)

        row = index + 2
        while row < len(lines) and "|" in lines[row] and lines[row].strip():
            label_columns_by_row[row] = label_columns
            row += 1
        index = row
    return header_lines, label_columns_by_row


def _find_untagged_claims(text: str) -> list[Finding]:
    """Flag likely claims; exact coverage is only possible in MemoArtifact JSON."""
    findings: list[Finding] = []
    in_fence = False
    current_heading = ""
    lines = text.splitlines()
    table_header_lines, table_label_columns = _table_layout(lines)
    for line_index, raw_line in enumerate(lines):
        line_number = line_index + 1
        stripped = raw_line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped or line_index in table_header_lines:
            continue
        heading = re.match(r"^#{1,6}\s+(.+?)\s*$", stripped)
        if heading:
            current_heading = heading.group(1).strip().lower()
            continue
        if current_heading in _NON_CLAIM_HEADINGS:
            continue
        if _TABLE_SEPARATOR.fullmatch(stripped):
            continue
        if _BOLD_SECTION_LABEL.fullmatch(stripped):
            continue

        is_table_row = line_index in table_label_columns
        fragments = _table_cells(stripped) if is_table_row else [stripped]
        for column, fragment in enumerate(fragments):
            if is_table_row and column in table_label_columns[line_index]:
                continue
            lowered = fragment.lower()
            if any(tag in lowered for tag in AXIS_A_TAGS):
                continue
            if "[basis:" in lowered:
                continue
            if _looks_like_material_claim(fragment):
                findings.append(
                    Finding(
                        "GTTA010",
                        Severity.WARNING,
                        "Likely material claim lacks an inline Axis A provenance tag."
                        + (
                            f" Table column: {column + 1}."
                            if is_table_row
                            else ""
                        ),
                        line_number,
                    )
                )
                if len(findings) == 25:
                    return findings
    return findings


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
        for aliases in _MODE_REQUIREMENTS[normalized_mode]:
            if not any(alias in lower_text for alias in aliases):
                findings.append(
                    Finding(
                        "GTTA008",
                        Severity.WARNING,
                        f"Mode {normalized_mode} output marker {aliases[0]!r} "
                        "was not found.",
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

    if normalized_mode != "F":
        findings.extend(_find_untagged_claims(text))

    return ContractReport(
        ruleset_version=RULESET_VERSION,
        mode=normalized_mode,
        evidence_mode=evidence_mode,
        findings=tuple(findings),
    )
