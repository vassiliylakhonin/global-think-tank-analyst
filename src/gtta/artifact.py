"""Structured memo artifact and its validation/rendering interface.

The claim ledger is the authoritative machine-readable surface. Markdown is a
rendered view: useful for people, but necessarily less exact to validate.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Any, Literal, Mapping

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)


ARTIFACT_SCHEMA_VERSION = "gtta.memo@1.0"


def _normalize_unique_refs(values: list[str], label: str) -> list[str]:
    normalized = [value.strip() for value in values]
    if any(not value for value in normalized):
        raise ValueError(f"{label} must not contain empty values")
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"{label} must be unique")
    return normalized


class MemoMode(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"


class EvidenceMode(str, Enum):
    LIVE_SOURCE_BACKED = "live-source-backed"
    USER_PROVIDED = "user-provided sources"
    ILLUSTRATIVE_PACKET = "illustrative source packet"
    REASONING_ONLY = "reasoning-only"


class Confidence(str, Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"


class ClaimKind(str, Enum):
    FACT = "fact"
    ASSESSMENT = "assessment"
    ASSUMPTION = "assumption"
    SCENARIO = "scenario"
    UNKNOWN = "unknown"


class Provenance(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    USER_PROVIDED = "user-provided"
    INFERENCE = "inference"
    ANALYST_JUDGMENT = "analyst-judgment"


class _ArtifactModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class MemoClaim(_ArtifactModel):
    claim_id: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9._-]{0,63}$")
    text: str = Field(min_length=1)
    kind: ClaimKind
    provenance: Provenance
    source_refs: list[str] = Field(default_factory=list)
    basis_claim_ids: list[str] = Field(default_factory=list)
    confidence: Confidence | None = None
    verify: bool = False
    stale_as_of: date | None = None

    @field_validator("source_refs", "basis_claim_ids")
    @classmethod
    def _unique_nonempty_refs(cls, values: list[str]) -> list[str]:
        return _normalize_unique_refs(values, "references")

    @model_validator(mode="after")
    def _source_backed_claims_name_sources(self) -> "MemoClaim":
        if self.kind is ClaimKind.FACT and self.provenance in {
            Provenance.INFERENCE,
            Provenance.ANALYST_JUDGMENT,
        }:
            raise ValueError("fact claims require source-backed provenance")
        if self.provenance in {
            Provenance.PRIMARY,
            Provenance.SECONDARY,
            Provenance.USER_PROVIDED,
        }:
            if not self.source_refs:
                raise ValueError(
                    "source-backed claims require at least one source_ref"
                )
        return self


class NarrativeBlock(_ArtifactModel):
    """Human-readable synthesis linked to the atomic claims it summarizes."""

    text: str = Field(min_length=1)
    claim_ids: list[str] = Field(default_factory=list)

    @field_validator("claim_ids")
    @classmethod
    def _unique_nonempty_claim_ids(cls, values: list[str]) -> list[str]:
        return _normalize_unique_refs(values, "claim_ids")


class DecisionOption(_ArtifactModel):
    option_id: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9._-]{0,63}$")
    title: str = Field(min_length=1)
    benefit: str = Field(min_length=1)
    downside: str = Field(min_length=1)
    conditions: str = Field(min_length=1)
    basis_claim_ids: list[str] = Field(default_factory=list)

    @field_validator("basis_claim_ids")
    @classmethod
    def _unique_basis_claim_ids(cls, values: list[str]) -> list[str]:
        return _normalize_unique_refs(values, "basis_claim_ids")


class WatchIndicator(_ArtifactModel):
    indicator_id: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9._-]{0,63}$")
    indicator: str = Field(min_length=1)
    trigger: str = Field(min_length=1)
    posture_change: str = Field(min_length=1)
    basis_claim_ids: list[str] = Field(default_factory=list)

    @field_validator("basis_claim_ids")
    @classmethod
    def _unique_basis_claim_ids(cls, values: list[str]) -> list[str]:
        return _normalize_unique_refs(values, "basis_claim_ids")


MODE_SECTION_KEYS: dict[MemoMode, tuple[str, ...]] = {
    MemoMode.A: ("main_risks", "what_to_watch"),
    MemoMode.B: ("actors",),
    MemoMode.C: ("baseline", "scenarios", "triggers"),
    MemoMode.D: ("target_claim", "alternative_explanations", "revised_judgment"),
    MemoMode.E: ("questions_for_owners",),
    MemoMode.F: ("coaching",),
    MemoMode.G: ("hypotheses", "evidence_matrix", "sensitivity", "bounded_judgment"),
}


class MemoArtifact(_ArtifactModel):
    schema_version: Literal["gtta.memo@1.0"]
    artifact_id: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9._-]{0,127}$")
    title: str = Field(min_length=1)
    question: str = Field(min_length=1)
    decision: str = Field(min_length=1)
    audience: str = Field(min_length=1)
    time_horizon: str = Field(min_length=1)
    mode: MemoMode
    evidence_mode: EvidenceMode
    bottom_line: NarrativeBlock
    claims: list[MemoClaim] = Field(default_factory=list)
    sections: dict[str, NarrativeBlock] = Field(default_factory=dict)
    options: list[DecisionOption] = Field(default_factory=list)
    indicators: list[WatchIndicator] = Field(default_factory=list)
    confidence: Confidence
    key_unknowns: list[str] = Field(default_factory=list)
    change_conditions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)

    @field_validator("sections")
    @classmethod
    def _normalize_sections(
        cls, sections: dict[str, NarrativeBlock]
    ) -> dict[str, NarrativeBlock]:
        normalized = {key.strip(): value for key, value in sections.items()}
        if any(not key for key in normalized):
            raise ValueError("section keys must not be empty")
        return normalized

    @field_validator("key_unknowns", "change_conditions", "limitations")
    @classmethod
    def _nonempty_items(cls, values: list[str]) -> list[str]:
        normalized = [value.strip() for value in values]
        if any(not value for value in normalized):
            raise ValueError("list items must not be empty")
        return normalized

    @model_validator(mode="after")
    def _enforce_artifact_contract(self) -> "MemoArtifact":
        if self.mode is not MemoMode.F and not self.claims:
            raise ValueError("modes A-E and G require at least one ledger claim")

        required_sections = set(MODE_SECTION_KEYS[self.mode])
        missing_sections = sorted(required_sections - self.sections.keys())
        if missing_sections:
            raise ValueError(
                "missing mode sections: " + ", ".join(missing_sections)
            )

        if self.mode in {MemoMode.B, MemoMode.E} and not self.options:
            raise ValueError(f"mode {self.mode.value} requires at least one option")
        if self.mode in {MemoMode.C, MemoMode.E} and not self.indicators:
            raise ValueError(f"mode {self.mode.value} requires at least one indicator")
        if self.mode in {MemoMode.B, MemoMode.E, MemoMode.G}:
            if not self.change_conditions:
                raise ValueError(
                    f"mode {self.mode.value} requires change_conditions"
                )

        identifiers = [claim.claim_id for claim in self.claims]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("claim_id values must be unique")
        option_ids = [option.option_id for option in self.options]
        if len(option_ids) != len(set(option_ids)):
            raise ValueError("option_id values must be unique")
        indicator_ids = [indicator.indicator_id for indicator in self.indicators]
        if len(indicator_ids) != len(set(indicator_ids)):
            raise ValueError("indicator_id values must be unique")

        known_claims = set(identifiers)
        for claim in self.claims:
            missing_basis = set(claim.basis_claim_ids) - known_claims
            if missing_basis:
                raise ValueError(
                    f"claim {claim.claim_id!r} references unknown basis claims: "
                    + ", ".join(sorted(missing_basis))
                )
            if claim.claim_id in claim.basis_claim_ids:
                raise ValueError(f"claim {claim.claim_id!r} cannot cite itself")

        dependency_graph = {
            claim.claim_id: claim.basis_claim_ids for claim in self.claims
        }
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(claim_id: str) -> None:
            if claim_id in visiting:
                raise ValueError(f"claim dependency cycle includes {claim_id!r}")
            if claim_id in visited:
                return
            visiting.add(claim_id)
            for basis_id in dependency_graph[claim_id]:
                visit(basis_id)
            visiting.remove(claim_id)
            visited.add(claim_id)

        for claim_id in dependency_graph:
            visit(claim_id)

        claim_references = {
            "bottom_line": self.bottom_line.claim_ids,
            **{
                f"sections.{key}": block.claim_ids
                for key, block in self.sections.items()
            },
            **{
                f"options.{option.option_id}": option.basis_claim_ids
                for option in self.options
            },
            **{
                f"indicators.{indicator.indicator_id}": indicator.basis_claim_ids
                for indicator in self.indicators
            },
        }
        used_claims: set[str] = set()
        for owner, claim_ids in claim_references.items():
            missing_claims = set(claim_ids) - known_claims
            if missing_claims:
                raise ValueError(
                    f"{owner} references unknown claims: "
                    + ", ".join(sorted(missing_claims))
                )
            used_claims.update(claim_ids)
        orphaned_claims = known_claims - used_claims
        if orphaned_claims:
            raise ValueError(
                "ledger claims must be used by the rendered memo: "
                + ", ".join(sorted(orphaned_claims))
            )

        if self.evidence_mode is EvidenceMode.REASONING_ONLY:
            sourced = [
                claim.claim_id
                for claim in self.claims
                if claim.provenance
                in {
                    Provenance.PRIMARY,
                    Provenance.SECONDARY,
                    Provenance.USER_PROVIDED,
                }
            ]
            if sourced:
                raise ValueError(
                    "reasoning-only artifacts cannot claim source-backed "
                    "provenance: " + ", ".join(sourced)
                )
        if self.evidence_mode is EvidenceMode.LIVE_SOURCE_BACKED:
            if not any(
                claim.provenance in {Provenance.PRIMARY, Provenance.SECONDARY}
                for claim in self.claims
            ):
                raise ValueError(
                    "live-source-backed artifacts require a primary or secondary claim"
                )
        if self.evidence_mode is EvidenceMode.USER_PROVIDED:
            if not any(
                claim.provenance is Provenance.USER_PROVIDED
                for claim in self.claims
            ):
                raise ValueError(
                    "user-provided sources artifacts require a user-provided claim"
                )
        return self


@dataclass(frozen=True)
class ArtifactFinding:
    code: str
    path: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


@dataclass(frozen=True)
class ArtifactReport:
    artifact: MemoArtifact | None
    findings: tuple[ArtifactFinding, ...]

    @property
    def passed(self) -> bool:
        return self.artifact is not None and not self.findings

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": ARTIFACT_SCHEMA_VERSION,
            "scope": "memo-artifact-structure-only",
            "passed": self.passed,
            "findings": [finding.to_dict() for finding in self.findings],
            "artifact": (
                self.artifact.model_dump(mode="json") if self.artifact else None
            ),
            "limitations": (
                "Artifact validation does not establish factuality or source support."
            ),
        }


def check_memo_artifact(payload: str | bytes | Mapping[str, Any]) -> ArtifactReport:
    """Parse and validate a memo artifact without raising on user input."""
    raw: Any = payload
    if isinstance(payload, (str, bytes)):
        try:
            raw = json.loads(payload)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            return ArtifactReport(
                artifact=None,
                findings=(
                    ArtifactFinding("ARTIFACT001", "$", f"Invalid JSON: {exc}"),
                ),
            )
    if not isinstance(raw, Mapping):
        return ArtifactReport(
            artifact=None,
            findings=(
                ArtifactFinding("ARTIFACT002", "$", "Artifact must be a JSON object."),
            ),
        )
    try:
        artifact = MemoArtifact.model_validate(raw)
    except ValidationError as exc:
        findings = tuple(
            ArtifactFinding(
                "ARTIFACT003",
                "$" + "".join(f"[{part!r}]" for part in error["loc"]),
                error["msg"],
            )
            for error in exc.errors(include_url=False)
        )
        return ArtifactReport(artifact=None, findings=findings)
    return ArtifactReport(artifact=artifact, findings=())


def get_memo_artifact_schema() -> dict[str, Any]:
    """Return the versioned JSON Schema for integrations and agent toolchains."""
    return MemoArtifact.model_json_schema()


_SECTION_TITLES = {
    "main_risks": "Main risks",
    "what_to_watch": "What to watch",
    "actors": "Actors and incentives",
    "baseline": "Baseline",
    "scenarios": "Scenarios",
    "triggers": "Triggers",
    "target_claim": "Target claim",
    "alternative_explanations": "Alternative explanations",
    "revised_judgment": "Revised judgment",
    "questions_for_owners": "Questions for owners",
    "coaching": "Coaching questions",
    "hypotheses": "Hypotheses",
    "evidence_matrix": "Evidence matrix",
    "sensitivity": "Sensitivity",
    "bounded_judgment": "Bounded judgment",
}


def render_memo_artifact(artifact: MemoArtifact) -> str:
    """Render the canonical human-readable view of a validated artifact."""
    claims_by_id = {claim.claim_id: claim for claim in artifact.claims}

    def render_block(block: NarrativeBlock) -> str:
        provenances = sorted(
            {claims_by_id[claim_id].provenance.value for claim_id in block.claim_ids}
        )
        tags = "".join(f"[{provenance}]" for provenance in provenances)
        basis = ", ".join(block.claim_ids)
        prefix = f"{tags} " if tags else ""
        suffix = f" [basis: {basis}]" if basis else ""
        return f"{prefix}{block.text}{suffix}"

    def render_basis(claim_ids: list[str]) -> str:
        if not claim_ids:
            return ""
        provenances = sorted(
            {claims_by_id[claim_id].provenance.value for claim_id in claim_ids}
        )
        tags = "".join(f"[{provenance}]" for provenance in provenances)
        return f" {tags} [basis: {', '.join(claim_ids)}]"

    takeaway_heading = (
        "Executive takeaway"
        if artifact.mode in {MemoMode.B, MemoMode.E}
        else "Bottom line"
    )
    lines = [
        f"# {artifact.title}",
        "",
        f"**Question:** {artifact.question}",
        f"**Decision:** {artifact.decision}",
        f"**Audience:** {artifact.audience}",
        f"**Time horizon:** {artifact.time_horizon}",
        f"**Evidence mode:** {artifact.evidence_mode.value}",
        f"**Depth:** Mode {artifact.mode.value}",
        "",
        f"## {takeaway_heading}",
        "",
        render_block(artifact.bottom_line),
        "",
        "## Decision context",
        "",
        f"**Decision:** {artifact.decision}",
    ]

    ordered_keys = list(MODE_SECTION_KEYS[artifact.mode])
    ordered_keys.extend(key for key in artifact.sections if key not in ordered_keys)
    for key in ordered_keys:
        lines.extend(
            ["", f"## {_SECTION_TITLES.get(key, key.replace('_', ' ').title())}", ""]
        )
        lines.append(render_block(artifact.sections[key]))

    if artifact.claims:
        lines.extend(["", "## Claim ledger", ""])
        for claim in artifact.claims:
            tags = f"[{claim.provenance.value}]"
            if claim.verify:
                tags += "[verify]"
            if claim.stale_as_of:
                tags += f"[stale-risk: {claim.stale_as_of.isoformat()}]"
            suffix = ""
            if claim.source_refs:
                suffix = " Sources: " + ", ".join(claim.source_refs) + "."
            lines.append(f"- `{claim.claim_id}` {tags} {claim.text}{suffix}")

    if artifact.options:
        lines.extend(["", "## Options", ""])
        for option in artifact.options:
            lines.extend(
                [
                    f"### {option.title} (`{option.option_id}`)",
                    "",
                    f"- **Benefit:** {option.benefit}{render_basis(option.basis_claim_ids)}",
                    f"- **Downside:** {option.downside}{render_basis(option.basis_claim_ids)}",
                    f"- **Conditions:** {option.conditions}{render_basis(option.basis_claim_ids)}",
                ]
            )

    if artifact.indicators:
        watch_heading = "Watchlist" if artifact.mode is MemoMode.E else "Indicators"
        lines.extend(["", f"## {watch_heading}", ""])
        for indicator in artifact.indicators:
            lines.append(
                f"- `{indicator.indicator_id}` {indicator.indicator} — trigger: "
                f"{indicator.trigger}; posture change: {indicator.posture_change}"
                f"{render_basis(indicator.basis_claim_ids)}"
            )

    lines.extend(["", "## Confidence", "", f"**Confidence: {artifact.confidence.value}.**"])
    if artifact.key_unknowns:
        lines.extend(["", "### Key unknowns", ""])
        lines.extend(f"- {item}" for item in artifact.key_unknowns)
    if artifact.change_conditions:
        lines.extend(["", "## What would change the judgment", ""])
        lines.extend(
            f"- **Change condition:** {item}" for item in artifact.change_conditions
        )
    if artifact.limitations:
        lines.extend(["", "## Limitations", ""])
        lines.extend(f"- {item}" for item in artifact.limitations)
    return "\n".join(lines).rstrip() + "\n"
