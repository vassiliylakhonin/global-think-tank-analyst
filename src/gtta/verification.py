"""MemoArtifact-to-Agenda evidence verification bridge.

The module owns projection and orchestration at the composition seam. Agenda
Intelligence remains the owner of source extraction, lexical checking, and
review rendering; GTTA does not copy those implementations.
"""

from __future__ import annotations

import html
import json
import os
import re
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any, Callable, Literal, Mapping

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from .artifact import MemoArtifact, Provenance

SOURCE_BACKED_PROVENANCE = {
    Provenance.PRIMARY,
    Provenance.SECONDARY,
    Provenance.USER_PROVIDED,
}
SOURCE_CATALOG_VERSION = "gtta.sources@1.0"
_SOURCE_CATALOG_SCHEMA_RESOURCE = "contracts/gtta.sources-1.0.schema.json"
_NUMBER_RE = re.compile(r"(?<!\w)[+-]?\d[\d.,]*(?:\s?%|\b)")
_HIGH_RISK_RE = re.compile(
    r"\b(?:sanctions?|sanctioned|designation|restricted[- ]party|regulat(?:ion|ory)|"
    r"statute|decree|law|legal|export controls?|санкци(?:я|и|онн\w*)|"
    r"регламент\w*|постановлен\w*|закон\w*|правов\w*)\b",
    re.IGNORECASE,
)


class VerificationDependencyError(RuntimeError):
    """Agenda Intelligence is not installed for the optional verification seam."""


class VerificationInputError(ValueError):
    """A source-backed artifact cannot safely be projected for verification."""


class _CatalogModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class SourceQuote(_CatalogModel):
    claim_id: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9._-]{0,63}$")
    source_id: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9._-]{0,127}$")
    text: str = Field(min_length=1)


class MemoSource(_CatalogModel):
    source_id: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9._-]{0,127}$")
    path: str = Field(min_length=1)
    title: str | None = None
    url: str | None = None


class MemoSourceCatalog(_CatalogModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        json_schema_extra={
            "$id": "urn:gtta:schema:sources:1.0",
            "$schema": "https://json-schema.org/draft/2020-12/schema",
        },
    )

    schema_version: Literal["gtta.sources@1.0"]
    sources: list[MemoSource] = Field(default_factory=list)
    quotes: list[SourceQuote] = Field(default_factory=list)

    @model_validator(mode="after")
    def _unique_source_ids(self) -> "MemoSourceCatalog":
        source_ids = [source.source_id for source in self.sources]
        if len(source_ids) != len(set(source_ids)):
            raise ValueError("source_id values must be unique")
        return self


def load_source_catalog(
    payload: str | bytes | Mapping[str, Any],
) -> MemoSourceCatalog:
    """Parse the versioned source sidecar without exposing Pydantic internals."""

    raw: Any = payload
    if isinstance(payload, (str, bytes)):
        try:
            raw = json.loads(payload)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise VerificationInputError(f"Invalid source catalog JSON: {exc}") from exc
    if not isinstance(raw, Mapping):
        raise VerificationInputError("Memo source catalog must be a JSON object")
    try:
        return MemoSourceCatalog.model_validate(raw)
    except ValidationError as exc:
        details = "; ".join(error["msg"] for error in exc.errors(include_url=False))
        raise VerificationInputError(f"Invalid memo source catalog: {details}") from exc


def get_memo_source_catalog_schema() -> dict[str, Any]:
    """Return the frozen JSON Schema shipped with the package."""

    schema_path = resources.files("gtta").joinpath(_SOURCE_CATALOG_SCHEMA_RESOURCE)
    return json.loads(schema_path.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class VerificationFinding:
    rule_id: str
    claim_id: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "rule_id": self.rule_id,
            "severity": "warning",
            "claim_id": self.claim_id,
            "message": self.message,
        }


@dataclass(frozen=True)
class MemoVerificationReport:
    packet: dict[str, Any]
    agenda_result: dict[str, Any]
    findings: tuple[VerificationFinding, ...]
    strict: bool

    @property
    def packet_status(self) -> str:
        response = self.agenda_result.get("response") or {}
        return str(response.get("packet_status") or "invalid")

    @property
    def passed(self) -> bool:
        if not self.agenda_result.get("valid"):
            return False
        if not self.strict:
            return True
        return self.packet_status == "packet_complete" and not self.findings

    def to_dict(self) -> dict[str, Any]:
        """Return an auditable result without repeating caller source text."""

        return {
            "interface": "gtta.memo-verification@1.0",
            "source_catalog_version": SOURCE_CATALOG_VERSION,
            "scope": "memo-artifact-to-evidence-packet-preflight",
            "strict": self.strict,
            "passed": self.passed,
            "packet_status": self.packet_status,
            "projected_claim_ids": [
                claim["claim_id"] for claim in self.packet.get("claims", [])
            ],
            "loaded_source_ids": [
                source["source_id"] for source in self.packet.get("sources", [])
            ],
            "gtta_findings": [finding.to_dict() for finding in self.findings],
            "agenda": self.agenda_result,
            "human_review_required": True,
            "limitations": (
                "Passing establishes packet completeness under deterministic "
                "structural and lexical checks, not factual truth, source authority, "
                "legal sufficiency, or decision safety."
            ),
        }

    def render_text(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        lines = [
            f"GTTA memo verification: {status}",
            f"Agenda packet status: {self.packet_status}",
            f"Projected claims: {len(self.packet.get('claims', []))}",
            f"Loaded sources: {len(self.packet.get('sources', []))}",
        ]
        for finding in self.findings:
            lines.append(
                f"- WARNING {finding.rule_id} {finding.claim_id}: {finding.message}"
            )
        response = self.agenda_result.get("response") or {}
        for action in response.get("owner_actions", []):
            lines.append(f"- ACTION: {action}")
        for error in self.agenda_result.get("errors", []):
            lines.append(f"- ERROR: {error}")
        lines.extend(
            [
                "Human review required: yes",
                "Limit: packet completeness only; factual truth was not assessed.",
            ]
        )
        return "\n".join(lines)


def _load_agenda_dependencies() -> (
    tuple[Callable[[dict[str, Any]], dict[str, Any]], Callable[[Path], str]]
):
    try:
        from agenda_intelligence.evidence_review import read_document_text
        from agenda_intelligence.services import check_evidence_packet
    except ImportError as exc:
        raise VerificationDependencyError(
            'Memo verification requires: pip install "global-think-tank-analyst[verification]"'
        ) from exc
    return check_evidence_packet, read_document_text


def _safe_source_path(base_dir: Path, value: str) -> Path:
    base = base_dir.resolve()
    candidate = (base / value).resolve()
    try:
        inside = os.path.commonpath((str(base), str(candidate))) == str(base)
    except ValueError:
        inside = False
    if not inside:
        raise VerificationInputError(
            f"Source path must stay inside the memo source catalog directory: {value}"
        )
    return candidate


def _verification_findings(
    artifact: MemoArtifact,
) -> tuple[VerificationFinding, ...]:
    findings: list[VerificationFinding] = []
    for claim in artifact.claims:
        if claim.provenance not in SOURCE_BACKED_PROVENANCE or claim.verify:
            continue
        is_risky = bool(
            _NUMBER_RE.search(claim.text) or _HIGH_RISK_RE.search(claim.text)
        )
        has_dated_primary_basis = (
            claim.provenance is Provenance.PRIMARY and claim.stale_as_of is not None
        )
        if is_risky and not has_dated_primary_basis:
            findings.append(
                VerificationFinding(
                    rule_id="GTTAV001",
                    claim_id=claim.claim_id,
                    message=(
                        "Risk-sensitive regulatory, sanctions, legal, or quantitative "
                        "claim lacks verify=true and a dated primary-source basis."
                    ),
                )
            )
    return tuple(findings)


def build_evidence_packet(
    artifact: MemoArtifact,
    *,
    source_catalog: MemoSourceCatalog,
    base_dir: Path,
    source_loader: Callable[[Path], str],
) -> dict[str, Any]:
    """Project source-backed ledger claims into Agenda's stable packet contract."""

    claims = [
        claim
        for claim in artifact.claims
        if claim.provenance in SOURCE_BACKED_PROVENANCE
    ]
    if not claims:
        raise VerificationInputError(
            "MemoArtifact has no source-backed claims to verify; reasoning-only "
            "judgments remain outside the evidence-packet seam."
        )

    referenced_source_ids = {
        source_id for claim in claims for source_id in claim.source_refs
    }
    source_records = {
        source.source_id: source
        for source in source_catalog.sources
        if source.source_id in referenced_source_ids
    }

    known_claim_ids = {claim.claim_id for claim in claims}
    unknown_quote_claim_ids = sorted(
        {quote.claim_id for quote in source_catalog.quotes} - known_claim_ids
    )
    if unknown_quote_claim_ids:
        raise VerificationInputError(
            "Source catalog quotes reference claims outside the evidence seam: "
            + ", ".join(unknown_quote_claim_ids)
        )

    packet_sources: list[dict[str, str]] = []
    for source_id in sorted(source_records):
        source = source_records[source_id]
        path = _safe_source_path(base_dir, source.path)
        try:
            text = source_loader(path)
        except Exception as exc:
            raise VerificationInputError(
                f"Cannot load source {source_id!r} from {source.path!r}: {exc}"
            ) from exc
        item = {"source_id": source_id, "text": text}
        if source.title is not None:
            item["title"] = source.title
        if source.url is not None:
            item["url"] = source.url
        packet_sources.append(item)

    packet_claims: list[dict[str, Any]] = []
    for claim in claims:
        item: dict[str, Any] = {
            "claim_id": claim.claim_id,
            "text": claim.text,
            "source_ids": list(claim.source_refs),
        }
        quotes = [
            {"source_id": quote.source_id, "text": quote.text}
            for quote in source_catalog.quotes
            if quote.claim_id == claim.claim_id
        ]
        if quotes:
            item["quotes"] = quotes
        packet_claims.append(item)

    return {
        "packet_id": artifact.artifact_id,
        "topic": artifact.title,
        "claims": packet_claims,
        "sources": packet_sources,
    }


def verify_memo_artifact(
    artifact: MemoArtifact,
    *,
    source_catalog: MemoSourceCatalog | None = None,
    base_dir: Path,
    strict: bool = False,
    checker: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
    source_loader: Callable[[Path], str] | None = None,
) -> MemoVerificationReport:
    """Project and check a memo through Agenda Intelligence's owned interface."""

    if checker is None or source_loader is None:
        default_checker, default_loader = _load_agenda_dependencies()
        checker = checker or default_checker
        source_loader = source_loader or default_loader
    packet = build_evidence_packet(
        artifact,
        source_catalog=source_catalog
        or MemoSourceCatalog(schema_version=SOURCE_CATALOG_VERSION),
        base_dir=base_dir,
        source_loader=source_loader,
    )
    result = checker(packet)
    return MemoVerificationReport(
        packet=packet,
        agenda_result=result,
        findings=_verification_findings(artifact),
        strict=strict,
    )


def render_verification_markdown(report: MemoVerificationReport) -> str:
    try:
        from agenda_intelligence.evidence_review import render_review_markdown
    except ImportError as exc:
        raise VerificationDependencyError(
            'Memo verification requires: pip install "global-think-tank-analyst[verification]"'
        ) from exc
    response = report.agenda_result.get("response")
    if not isinstance(response, dict):
        raise VerificationInputError(
            "Agenda Intelligence rejected the projected evidence-packet contract: "
            + "; ".join(str(error) for error in report.agenda_result.get("errors", []))
        )
    preflight = ["# GTTA verification preflight", ""]
    if report.findings:
        preflight.extend(
            f"- `{finding.rule_id}` `{finding.claim_id}` — {finding.message}"
            for finding in report.findings
        )
    else:
        preflight.append("- No GTTA verification-marker findings.")
    preflight.extend(["", render_review_markdown(report.packet, response)])
    return "\n".join(preflight)


def render_verification_html(report: MemoVerificationReport) -> str:
    try:
        from agenda_intelligence.evidence_review import render_review_html
    except ImportError as exc:
        raise VerificationDependencyError(
            'Memo verification requires: pip install "global-think-tank-analyst[verification]"'
        ) from exc
    response = report.agenda_result.get("response")
    if not isinstance(response, dict):
        raise VerificationInputError(
            "Agenda Intelligence rejected the projected evidence-packet contract: "
            + "; ".join(str(error) for error in report.agenda_result.get("errors", []))
        )
    rendered = render_review_html(report.packet, response)
    if not report.findings:
        return rendered
    items = "".join(
        "<li><code>"
        + html.escape(finding.rule_id)
        + "</code> <code>"
        + html.escape(finding.claim_id)
        + "</code> — "
        + html.escape(finding.message)
        + "</li>"
        for finding in report.findings
    )
    banner = (
        '<aside style="margin:1rem;padding:1rem;border:1px solid #d29922">'
        "<strong>GTTA verification preflight</strong><ul>" + items + "</ul></aside>"
    )
    return rendered.replace("<body>", "<body>" + banner, 1)


def render_memo_repair_prompt(report: MemoVerificationReport) -> str:
    """Render bounded repair guidance without embedding caller source text."""

    response = report.agenda_result.get("response") or {}
    needs_repair = report.packet_status != "packet_complete" or bool(report.findings)
    if not needs_repair:
        return (
            "# GTTA Memo Repair Status: Complete\n\n"
            "No deterministic declaration or packet-completeness repair is required. "
            "Human review is still required; factual truth and legal sufficiency were "
            "not assessed.\n"
        )

    lines = [
        "# GTTA Memo Repair Instructions",
        "",
        f"The deterministic preflight returned `{report.packet_status}`.",
        "Repair the declarations and claim scope; do not manufacture evidence.",
        "",
        "## Non-negotiable safety constraints",
        "",
        "- Use only source files already supplied by the operator, or stop and request the missing source.",
        "- Never invent a source ID, path, URL, quotation, date, number, designation, regulation, or factual assertion.",
        "- Never rewrite a claim merely to mimic an irrelevant source or to make lexical matching pass.",
        "- Preserve `gtta.memo@1.0` and `gtta.sources@1.0`; keep inference and analyst judgment outside the evidence packet.",
        "- A `[verify]` / `verify: true` marker records unresolved checking work; it is not evidence and must not be described as verification.",
        "",
        "## Allowed repair actions",
        "",
        "1. Attach an operator-supplied source that directly supports the claim.",
        "2. Correct a source reference or quote only after checking the supplied file; quotes must be exact.",
        "3. Narrow, qualify, split, or remove an unsupported claim.",
        "4. Reclassify genuine reasoning as `inference` or `analyst-judgment` and preserve its basis links.",
        "5. Add `verify: true` when the claim still requires current primary-source checking.",
        "6. If no safe repair is possible, keep the gap visible and request evidence from the operator.",
        "",
        "## Claim-specific diagnostics",
        "",
    ]

    diagnostic_count = 0
    for finding in report.findings:
        diagnostic_count += 1
        lines.append(
            f"- `{finding.claim_id}` — `{finding.rule_id}`: {finding.message}"
        )

    claim_results = response.get("claims", [])
    if isinstance(claim_results, list):
        for item in claim_results:
            if not isinstance(item, Mapping):
                continue
            status = str(item.get("packet_status") or "unknown")
            if status == "packet_complete":
                continue
            diagnostic_count += 1
            claim_id = str(item.get("claim_id") or "unknown")
            issues = item.get("issues") or []
            issue_text = ", ".join(str(issue) for issue in issues) or "unspecified"
            lines.append(
                f"- `{claim_id}` — `{status}`; issue codes: `{issue_text}`."
            )

    if diagnostic_count == 0:
        errors = report.agenda_result.get("errors") or []
        if errors:
            lines.extend(f"- Agenda contract error: {error}" for error in errors)
        else:
            lines.append("- Review the packet-level status and keep unresolved gaps visible.")

    lines.extend(
        [
            "",
            "## Expected result",
            "",
            "Return an updated MemoArtifact JSON and, if needed, its companion source-catalog JSON. "
            "Then rerun `gtta verify memo.json --strict`. Do not claim success unless that command "
            "passes, and do not treat a pass as factual truth or legal clearance.",
            "",
        ]
    )
    return "\n".join(lines)
