"""Opt-in v2 deterministic declarations and local snapshot checks."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from .harvest import SOURCE_ID, load_snapshots


class ReversalCondition(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    metric: str = Field(min_length=1)
    operator: Literal["<", "<=", "==", ">=", ">", "!="]
    threshold: float = Field(allow_inf_nan=False, strict=True)
    unit: str = Field(min_length=1)
    review_by: date
    action: str = Field(min_length=1)

    @field_validator("review_by", mode="before")
    @classmethod
    def exact_date(cls, value):
        if isinstance(value, str) and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError("review_by must be YYYY-MM-DD")
        return value


class DeclaredQuote(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    source_id: str = Field(pattern=rf"^{SOURCE_ID}$")
    quote: str = Field(min_length=1)


def blocks(text: str, label: str):
    """Only top-level, explicitly labelled JSON fences are declarations."""
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        opening = re.fullmatch(r"(`{3,}|~{3,})([^`~]*)", lines[index])
        if not opening:
            index += 1
            continue
        marker, info = opening.groups()
        start = index
        index += 1
        body = []
        while index < len(lines) and not re.fullmatch(
            re.escape(marker[0]) + "{" + str(len(marker)) + ",}\\s*", lines[index]
        ):
            body.append(lines[index])
            index += 1
        if info.strip() == label:
            yield start + 1, "\n".join(body), index < len(lines)
        index += 1


def prose_fragments(text: str):
    """Markdown declarations, not natural-language fact classification."""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence or line.lstrip().startswith("#"):
            continue
        for cell in line.split("|"):
            yield number, cell


def null_hypothesis_present(text: str) -> bool:
    # A heading or mention alone is not a populated baseline.
    visible = "\n".join(fragment for _, fragment in prose_fragments(text))
    for line in visible.splitlines():
        match = re.match(
            r"^\s*(?:[-*]\s+)?(?:\*\*)?Null hypothesis(?:\*\*)?\s*:\s*(.+)", line, re.I
        )
        if match:
            body = match.group(1).strip().strip("*").strip()
            if len(body) >= 15 and not re.fullmatch(r"\[.*\]|TODO.*|TBD.*", body, re.I):
                return True
    return False


def strict_findings(text: str, mode: str | None, manifest: Path | None = None):
    from .discipline import Finding, Severity

    findings = []

    def error(rule, message, line=None):
        findings.append(Finding(rule, Severity.ERROR, message, line))

    if mode != "F" and not null_hypothesis_present(text):
        error(
            "GTTA011", "Declare a populated 'Null hypothesis: ...' no-action baseline."
        )

    citations = []
    for line, fragment in prose_fragments(text):
        refs = re.findall(rf"\[({SOURCE_ID})\]", fragment)
        citations.extend((line, ref) for ref in refs)
        if (
            any(
                tag in fragment.lower()
                for tag in ("[primary]", "[secondary]", "[user-provided]")
            )
            and not refs
        ):
            error(
                "GTTA012",
                "Declared source-backed fragment requires an inline [SRC-XX] reference.",
                line,
            )

    reversals = list(blocks(text, "gtta-reversals"))
    if mode in {"B", "E", "G"} and not reversals:
        error("GTTA013", "Deeper memo requires a gtta-reversals JSON block.")
    for line, body, closed in reversals:
        try:
            values = json.loads(body)
            if not closed or not isinstance(values, list) or not values:
                raise ValueError("expected a closed block containing a nonempty list")
            for value in values:
                ReversalCondition.model_validate(value)
        except (ValueError, ValidationError) as exc:
            error("GTTA013", f"Invalid reversal declaration: {exc}", line)

    quotes = []
    for line, body, closed in blocks(text, "gtta-quotes"):
        try:
            values = json.loads(body)
            if not closed or not isinstance(values, list) or not values:
                raise ValueError("expected a closed block containing a nonempty list")
            quotes.extend(
                (line, DeclaredQuote.model_validate(value)) for value in values
            )
        except (ValueError, ValidationError) as exc:
            error("GTTA014", f"Invalid quote declaration: {exc}", line)

    if manifest is not None:
        try:
            snapshots = load_snapshots(manifest)
        except (OSError, ValueError, LookupError) as exc:
            error("GTTA015", f"Cannot validate local snapshots: {exc}")
            return findings
        for line, ref in citations:
            if ref not in snapshots:
                error("GTTA015", f"Referenced snapshot is missing: {ref}", line)
        for line, quote in quotes:
            if (
                quote.source_id not in snapshots
                or quote.quote not in snapshots[quote.source_id]
            ):
                error(
                    "GTTA014",
                    f"Declared quote is absent from snapshot {quote.source_id}.",
                    line,
                )
    elif quotes:
        error(
            "GTTA015",
            "Declared quotes require a local --sources manifest for literal checking.",
        )
    return findings
