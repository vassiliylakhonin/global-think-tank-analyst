"""Build and check an auditable review bundle from a MemoArtifact.

This module owns the bundle lifecycle only. Memo validation remains in
``gtta.artifact``; claim/source checking and review rendering remain at the
Agenda Intelligence seam exposed by ``gtta.verification``.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .artifact import (
    ARTIFACT_SCHEMA_VERSION,
    EvidenceMode,
    MemoArtifact,
    MemoMode,
    check_memo_artifact,
    render_memo_artifact,
)
from .sarif import render_verification_sarif
from .verification import (
    MEMO_VERIFICATION_VERSION,
    SOURCE_CATALOG_VERSION,
    MemoSourceCatalog,
    MemoVerificationReport,
    load_source_catalog,
    render_memo_repair_prompt,
    render_verification_html,
    render_verification_markdown,
    verify_memo_artifact,
)


REVIEW_BUNDLE_VERSION = "gtta.review-bundle@1.0"
REVIEW_BUNDLE_CHECK_VERSION = "gtta.review-bundle-check@1.0"
_REVIEW_OUTPUT_MEDIA_TYPES = {
    "memo.md": "text/markdown",
    "verification.json": "application/json",
    "verification.md": "text/markdown",
    "review.html": "text/html",
    "verification.sarif": "application/sarif+json",
    "repair.md": "text/markdown",
}
_REVIEW_BUNDLE_FILENAMES = frozenset(
    {"manifest.json", *_REVIEW_OUTPUT_MEDIA_TYPES}
)
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ReviewBundleInputError(ValueError):
    """The requested review bundle cannot be created safely."""


class ReviewBundleAccessError(OSError):
    """A review bundle cannot be accessed safely enough to check it."""


@dataclass(frozen=True)
class ReviewBundleFinding:
    """One deterministic review-bundle contract violation."""

    rule_id: str
    path: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "rule_id": self.rule_id,
            "severity": "error",
            "path": self.path,
            "message": self.message,
        }


@dataclass(frozen=True)
class ReviewBundleCheckReport:
    """Integrity and consistency result for one published review bundle."""

    bundle_dir: Path
    bundle_interface: str | None
    verification_passed: bool | None
    packet_status: str | None
    findings: tuple[ReviewBundleFinding, ...]

    @property
    def passed(self) -> bool:
        return not self.findings

    def to_dict(self) -> dict[str, Any]:
        return {
            "interface": REVIEW_BUNDLE_CHECK_VERSION,
            "scope": "review-bundle-integrity-and-consistency",
            "bundle": self.bundle_dir.as_posix(),
            "bundle_interface": self.bundle_interface,
            "passed": self.passed,
            "verification_passed": self.verification_passed,
            "packet_status": self.packet_status,
            "finding_count": len(self.findings),
            "findings": [finding.to_dict() for finding in self.findings],
            "limitations": (
                "Checks the bundle contract, internal consistency, and SHA-256 "
                "integrity. Hashes are not signatures and do not establish "
                "authenticity, provenance, factual truth, or decision safety."
            ),
        }

    def render_text(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        lines = [
            f"GTTA review bundle integrity: {status}",
            f"Bundle: {self.bundle_dir}",
            f"Interface: {self.bundle_interface or 'unavailable'}",
            (
                "Recorded verification: unavailable"
                if self.verification_passed is None
                else "Recorded verification: "
                + ("PASS" if self.verification_passed else "REVIEW REQUIRED")
            ),
            f"Packet status: {self.packet_status or 'unavailable'}",
        ]
        lines.extend(
            f"- ERROR {finding.rule_id} {finding.path}: {finding.message}"
            for finding in self.findings
        )
        lines.append(
            "Limit: SHA-256 integrity is not a signature or proof of authenticity."
        )
        return "\n".join(lines)


@dataclass(frozen=True)
class ReviewBundleResult:
    """Result of writing a complete review bundle."""

    output_dir: Path
    report: MemoVerificationReport
    manifest: dict[str, Any]


def _sha256(value: str | bytes) -> str:
    data = value.encode("utf-8") if isinstance(value, str) else value
    return hashlib.sha256(data).hexdigest()


def _with_final_newline(value: str) -> str:
    return value if value.endswith("\n") else value + "\n"


def _read_text(path: Path, label: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ReviewBundleInputError(f"Cannot read {label} {path}: {exc}") from exc


def _load_artifact(path: Path) -> tuple[str, MemoArtifact]:
    artifact_text = _read_text(path, "MemoArtifact")
    artifact_report = check_memo_artifact(artifact_text)
    if not artifact_report.passed or artifact_report.artifact is None:
        details = "; ".join(
            f"{finding.code} {finding.path}: {finding.message}"
            for finding in artifact_report.findings
        )
        raise ReviewBundleInputError(f"Invalid MemoArtifact: {details}")
    return artifact_text, artifact_report.artifact


def _load_catalog(
    artifact_path: Path, source_catalog_path: Path | None
) -> tuple[MemoSourceCatalog, Path, Path | None, str | None]:
    catalog_path = source_catalog_path
    if catalog_path is None:
        candidate = artifact_path.with_name(artifact_path.stem + ".sources.json")
        if candidate.is_file():
            catalog_path = candidate
    if catalog_path is None:
        return (
            MemoSourceCatalog(schema_version=SOURCE_CATALOG_VERSION),
            artifact_path.parent,
            None,
            None,
        )
    catalog_text = _read_text(catalog_path, "source catalog")
    return (
        load_source_catalog(catalog_text),
        catalog_path.parent,
        catalog_path,
        catalog_text,
    )


def _write_new_directory(output_dir: Path, files: dict[str, str]) -> None:
    if output_dir.exists():
        raise ReviewBundleInputError(
            f"Output directory already exists: {output_dir}. Choose a new --out-dir."
        )
    try:
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        staged = Path(
            tempfile.mkdtemp(
                prefix=f".{output_dir.name}.tmp-", dir=output_dir.parent
            )
        )
    except OSError as exc:
        raise ReviewBundleInputError(
            f"Cannot prepare output directory {output_dir}: {exc}"
        ) from exc
    try:
        for name, content in files.items():
            (staged / name).write_text(content, encoding="utf-8")
        if output_dir.exists():
            raise ReviewBundleInputError(
                f"Output directory appeared during review: {output_dir}"
            )
        staged.replace(output_dir)
    except Exception:
        shutil.rmtree(staged, ignore_errors=True)
        raise


def build_review_bundle(
    artifact_path: str | Path,
    *,
    source_catalog_path: str | Path | None = None,
    output_dir: str | Path | None = None,
    strict: bool = True,
) -> ReviewBundleResult:
    """Validate, verify, render, and atomically write one review directory.

    The directory is never overwritten. A failed deterministic verification
    still produces the complete bundle and returns ``report.passed == False``;
    invalid inputs or missing dependencies raise before publication.
    """

    artifact_file = Path(artifact_path).resolve()
    catalog_file = (
        Path(source_catalog_path).resolve()
        if source_catalog_path is not None
        else None
    )
    destination = (
        Path(output_dir).resolve()
        if output_dir is not None
        else artifact_file.with_name(artifact_file.stem + ".review")
    )
    if destination.exists():
        raise ReviewBundleInputError(
            f"Output directory already exists: {destination}. Choose a new --out-dir."
        )

    artifact_text, artifact = _load_artifact(artifact_file)
    catalog, base_dir, resolved_catalog, catalog_text = _load_catalog(
        artifact_file, catalog_file
    )
    report = verify_memo_artifact(
        artifact,
        source_catalog=catalog,
        base_dir=base_dir,
        strict=strict,
    )

    receipt = report.to_dict()
    rendered_files = {
        "memo.md": _with_final_newline(render_memo_artifact(artifact)),
        "verification.json": json.dumps(
            receipt, ensure_ascii=False, indent=2
        )
        + "\n",
        "verification.md": _with_final_newline(
            render_verification_markdown(report)
        ),
        "review.html": _with_final_newline(render_verification_html(report)),
        "verification.sarif": json.dumps(
            render_verification_sarif(
                report,
                artifact_uri=artifact_file.name,
                artifact_text=artifact_text,
            ),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        "repair.md": _with_final_newline(render_memo_repair_prompt(report)),
    }
    manifest: dict[str, Any] = {
        "interface": REVIEW_BUNDLE_VERSION,
        "verification_interface": MEMO_VERIFICATION_VERSION,
        "strict": strict,
        "passed": report.passed,
        "packet_status": report.packet_status,
        "human_review_required": True,
        "inputs": {
            "artifact": {
                "filename": artifact_file.name,
                "schema_version": artifact.schema_version,
                "artifact_id": artifact.artifact_id,
                "mode": artifact.mode.value,
                "evidence_mode": artifact.evidence_mode.value,
                "sha256": _sha256(artifact_text),
            },
            "source_catalog": (
                {
                    "filename": resolved_catalog.name,
                    "schema_version": catalog.schema_version,
                    "sha256": _sha256(catalog_text or ""),
                }
                if resolved_catalog is not None
                else None
            ),
            "loaded_sources": [
                {
                    "source_id": str(source.get("source_id") or "unknown"),
                    "sha256": _sha256(str(source.get("text") or "")),
                }
                for source in report.packet.get("sources", [])
            ],
        },
        "outputs": {
            name: {
                "media_type": _REVIEW_OUTPUT_MEDIA_TYPES[name],
                "sha256": _sha256(content),
            }
            for name, content in rendered_files.items()
        },
        "limitations": receipt["limitations"],
    }
    files = {
        **rendered_files,
        "manifest.json": json.dumps(
            manifest, ensure_ascii=False, indent=2, sort_keys=True
        )
        + "\n",
    }
    _write_new_directory(destination, files)
    return ReviewBundleResult(
        output_dir=destination,
        report=report,
        manifest=manifest,
    )


def _add_finding(
    findings: list[ReviewBundleFinding],
    rule_id: str,
    path: str,
    message: str,
) -> None:
    findings.append(
        ReviewBundleFinding(rule_id=rule_id, path=path, message=message)
    )


def _parse_json_object(
    content: bytes,
    *,
    path: str,
    label: str,
    rule_id: str,
    findings: list[ReviewBundleFinding],
) -> dict[str, Any] | None:
    try:
        value = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        _add_finding(findings, rule_id, path, f"Invalid {label} JSON: {exc}")
        return None
    if not isinstance(value, dict):
        _add_finding(findings, rule_id, path, f"{label} must be a JSON object")
        return None
    return value


def _valid_sha256(value: Any) -> bool:
    return isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None


def _check_input_manifest(
    manifest: Mapping[str, Any], findings: list[ReviewBundleFinding]
) -> None:
    inputs = manifest.get("inputs")
    if not isinstance(inputs, Mapping):
        _add_finding(
            findings,
            "GTTAB005",
            "manifest.json#/inputs",
            "inputs must be an object",
        )
        return

    artifact = inputs.get("artifact")
    if not isinstance(artifact, Mapping):
        _add_finding(
            findings,
            "GTTAB005",
            "manifest.json#/inputs/artifact",
            "artifact must be an object",
        )
    else:
        expected_values = {
            "schema_version": {ARTIFACT_SCHEMA_VERSION},
            "mode": {mode.value for mode in MemoMode},
            "evidence_mode": {mode.value for mode in EvidenceMode},
        }
        for field, allowed in expected_values.items():
            if artifact.get(field) not in allowed:
                _add_finding(
                    findings,
                    "GTTAB005",
                    f"manifest.json#/inputs/artifact/{field}",
                    f"Unsupported or missing artifact {field}",
                )
        for field in ("filename", "artifact_id"):
            value = artifact.get(field)
            if not isinstance(value, str) or not value:
                _add_finding(
                    findings,
                    "GTTAB005",
                    f"manifest.json#/inputs/artifact/{field}",
                    f"artifact {field} must be a non-empty string",
                )
        if not _valid_sha256(artifact.get("sha256")):
            _add_finding(
                findings,
                "GTTAB013",
                "manifest.json#/inputs/artifact/sha256",
                "artifact sha256 must be 64 lowercase hexadecimal characters",
            )

    catalog = inputs.get("source_catalog")
    if catalog is not None:
        if not isinstance(catalog, Mapping):
            _add_finding(
                findings,
                "GTTAB005",
                "manifest.json#/inputs/source_catalog",
                "source_catalog must be an object or null",
            )
        else:
            if catalog.get("schema_version") != SOURCE_CATALOG_VERSION:
                _add_finding(
                    findings,
                    "GTTAB005",
                    "manifest.json#/inputs/source_catalog/schema_version",
                    "Unsupported or missing source catalog schema_version",
                )
            if not isinstance(catalog.get("filename"), str) or not catalog.get(
                "filename"
            ):
                _add_finding(
                    findings,
                    "GTTAB005",
                    "manifest.json#/inputs/source_catalog/filename",
                    "source catalog filename must be a non-empty string",
                )
            if not _valid_sha256(catalog.get("sha256")):
                _add_finding(
                    findings,
                    "GTTAB013",
                    "manifest.json#/inputs/source_catalog/sha256",
                    "source catalog sha256 must be 64 lowercase hexadecimal characters",
                )

    loaded_sources = inputs.get("loaded_sources")
    if not isinstance(loaded_sources, list):
        _add_finding(
            findings,
            "GTTAB005",
            "manifest.json#/inputs/loaded_sources",
            "loaded_sources must be an array",
        )
        return
    source_ids: list[str] = []
    for index, source in enumerate(loaded_sources):
        path = f"manifest.json#/inputs/loaded_sources/{index}"
        if not isinstance(source, Mapping):
            _add_finding(
                findings, "GTTAB005", path, "loaded source must be an object"
            )
            continue
        source_id = source.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            _add_finding(
                findings,
                "GTTAB005",
                f"{path}/source_id",
                "source_id must be a non-empty string",
            )
        else:
            source_ids.append(source_id)
        if not _valid_sha256(source.get("sha256")):
            _add_finding(
                findings,
                "GTTAB013",
                f"{path}/sha256",
                "source sha256 must be 64 lowercase hexadecimal characters",
            )
    if len(source_ids) != len(set(source_ids)):
        _add_finding(
            findings,
            "GTTAB005",
            "manifest.json#/inputs/loaded_sources",
            "source_id values must be unique",
        )


def _check_output_manifest(
    manifest: Mapping[str, Any],
    contents: Mapping[str, bytes],
    findings: list[ReviewBundleFinding],
) -> None:
    outputs = manifest.get("outputs")
    if not isinstance(outputs, Mapping):
        _add_finding(
            findings,
            "GTTAB006",
            "manifest.json#/outputs",
            "outputs must be an object",
        )
        return
    expected_names = set(_REVIEW_OUTPUT_MEDIA_TYPES)
    declared_names = set(outputs)
    if declared_names != expected_names:
        missing = sorted(expected_names - declared_names)
        unexpected = sorted(declared_names - expected_names)
        details = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if unexpected:
            details.append("unexpected " + ", ".join(unexpected))
        _add_finding(
            findings,
            "GTTAB006",
            "manifest.json#/outputs",
            "Output declarations do not match the contract: " + "; ".join(details),
        )

    for name in sorted(expected_names & declared_names):
        metadata = outputs.get(name)
        path = f"manifest.json#/outputs/{name}"
        if not isinstance(metadata, Mapping):
            _add_finding(
                findings, "GTTAB007", path, "output metadata must be an object"
            )
            continue
        expected_media_type = _REVIEW_OUTPUT_MEDIA_TYPES[name]
        if metadata.get("media_type") != expected_media_type:
            _add_finding(
                findings,
                "GTTAB007",
                f"{path}/media_type",
                f"media_type must be {expected_media_type}",
            )
        digest = metadata.get("sha256")
        if not _valid_sha256(digest):
            _add_finding(
                findings,
                "GTTAB007",
                f"{path}/sha256",
                "sha256 must be 64 lowercase hexadecimal characters",
            )
        elif name in contents and _sha256(contents[name]) != digest:
            _add_finding(
                findings,
                "GTTAB008",
                name,
                "File content does not match the manifest sha256",
            )


def _check_receipt(
    receipt: Mapping[str, Any],
    manifest: Mapping[str, Any] | None,
    findings: list[ReviewBundleFinding],
) -> None:
    if receipt.get("interface") != MEMO_VERIFICATION_VERSION:
        _add_finding(
            findings,
            "GTTAB009",
            "verification.json#/interface",
            f"interface must be {MEMO_VERIFICATION_VERSION}",
        )
    if receipt.get("source_catalog_version") != SOURCE_CATALOG_VERSION:
        _add_finding(
            findings,
            "GTTAB009",
            "verification.json#/source_catalog_version",
            f"source_catalog_version must be {SOURCE_CATALOG_VERSION}",
        )
    if receipt.get("scope") != "memo-artifact-to-evidence-packet-preflight":
        _add_finding(
            findings,
            "GTTAB009",
            "verification.json#/scope",
            "scope must be memo-artifact-to-evidence-packet-preflight",
        )

    for field in ("projected_claim_ids", "loaded_source_ids"):
        values = receipt.get(field)
        if (
            not isinstance(values, list)
            or any(not isinstance(value, str) or not value for value in values)
            or len(values) != len(set(values))
        ):
            _add_finding(
                findings,
                "GTTAB009",
                f"verification.json#/{field}",
                f"{field} must contain unique non-empty strings",
            )

    strict = receipt.get("strict")
    passed = receipt.get("passed")
    packet_status = receipt.get("packet_status")
    gtta_findings = receipt.get("gtta_findings")
    agenda = receipt.get("agenda")
    if type(strict) is not bool:
        _add_finding(
            findings,
            "GTTAB009",
            "verification.json#/strict",
            "strict must be a boolean",
        )
    if type(passed) is not bool:
        _add_finding(
            findings,
            "GTTAB009",
            "verification.json#/passed",
            "passed must be a boolean",
        )
    if not isinstance(packet_status, str) or not packet_status:
        _add_finding(
            findings,
            "GTTAB009",
            "verification.json#/packet_status",
            "packet_status must be a non-empty string",
        )
    if not isinstance(gtta_findings, list):
        _add_finding(
            findings,
            "GTTAB009",
            "verification.json#/gtta_findings",
            "gtta_findings must be an array",
        )
    if receipt.get("human_review_required") is not True:
        _add_finding(
            findings,
            "GTTAB009",
            "verification.json#/human_review_required",
            "human_review_required must be true",
        )
    if not isinstance(receipt.get("limitations"), str) or not receipt.get(
        "limitations"
    ):
        _add_finding(
            findings,
            "GTTAB009",
            "verification.json#/limitations",
            "limitations must be a non-empty string",
        )

    agenda_valid: bool | None = None
    response_status: str | None = None
    if not isinstance(agenda, Mapping):
        _add_finding(
            findings,
            "GTTAB009",
            "verification.json#/agenda",
            "agenda must be an object",
        )
    else:
        if type(agenda.get("valid")) is bool:
            agenda_valid = agenda["valid"]
        else:
            _add_finding(
                findings,
                "GTTAB009",
                "verification.json#/agenda/valid",
                "Agenda valid must be a boolean",
            )
        response = agenda.get("response")
        if isinstance(response, Mapping):
            value = response.get("packet_status")
            if isinstance(value, str) and value:
                response_status = value
            else:
                _add_finding(
                    findings,
                    "GTTAB009",
                    "verification.json#/agenda/response/packet_status",
                    "Agenda response packet_status must be a non-empty string",
                )
            if response.get("human_review_required") is not True:
                _add_finding(
                    findings,
                    "GTTAB009",
                    "verification.json#/agenda/response/human_review_required",
                    "Agenda response human_review_required must be true",
                )
            if response.get("factuality_status") != "not_assessed":
                _add_finding(
                    findings,
                    "GTTAB009",
                    "verification.json#/agenda/response/factuality_status",
                    "Agenda response factuality_status must be not_assessed",
                )
        else:
            _add_finding(
                findings,
                "GTTAB009",
                "verification.json#/agenda/response",
                "Agenda response must be an object",
            )

    if (
        isinstance(packet_status, str)
        and response_status is not None
        and packet_status != response_status
    ):
        _add_finding(
            findings,
            "GTTAB010",
            "verification.json#/packet_status",
            "packet_status disagrees with Agenda response",
        )

    if (
        type(strict) is bool
        and type(passed) is bool
        and isinstance(packet_status, str)
        and isinstance(gtta_findings, list)
        and agenda_valid is not None
    ):
        expected_passed = agenda_valid and (
            not strict
            or (packet_status == "packet_complete" and not gtta_findings)
        )
        if passed is not expected_passed:
            _add_finding(
                findings,
                "GTTAB010",
                "verification.json#/passed",
                "passed disagrees with strict verification semantics",
            )

    if manifest is not None:
        comparisons = {
            "verification_interface": receipt.get("interface"),
            "strict": strict,
            "passed": passed,
            "packet_status": packet_status,
            "human_review_required": receipt.get("human_review_required"),
            "limitations": receipt.get("limitations"),
        }
        for field, receipt_value in comparisons.items():
            if manifest.get(field) != receipt_value:
                _add_finding(
                    findings,
                    "GTTAB010",
                    f"manifest.json#/{field}",
                    f"{field} disagrees with verification.json",
                )
        inputs = manifest.get("inputs")
        if isinstance(inputs, Mapping):
            loaded_sources = inputs.get("loaded_sources")
            if isinstance(loaded_sources, list) and all(
                isinstance(source, Mapping) for source in loaded_sources
            ):
                manifest_source_ids = [
                    source.get("source_id") for source in loaded_sources
                ]
                if manifest_source_ids != receipt.get("loaded_source_ids"):
                    _add_finding(
                        findings,
                        "GTTAB010",
                        "manifest.json#/inputs/loaded_sources",
                        "Loaded source IDs disagree with verification.json",
                    )


def check_review_bundle(bundle_dir: str | Path) -> ReviewBundleCheckReport:
    """Check a published bundle without requiring Agenda Intelligence.

    Contract or integrity failures are returned as findings. Missing,
    non-directory, or unreadable paths raise ``ReviewBundleAccessError`` so the
    CLI can distinguish an operational error from a bundle that failed review.
    """

    directory = Path(bundle_dir).absolute()
    findings: list[ReviewBundleFinding] = []
    try:
        if not directory.exists():
            raise ReviewBundleAccessError(
                f"Review bundle directory does not exist: {directory}"
            )
        if directory.is_symlink():
            _add_finding(
                findings,
                "GTTAB002",
                ".",
                "Review bundle directory must not be a symbolic link",
            )
            return ReviewBundleCheckReport(
                directory, None, None, None, tuple(findings)
            )
        if not directory.is_dir():
            raise ReviewBundleAccessError(
                f"Review bundle path is not a directory: {directory}"
            )
        entries = sorted(directory.iterdir(), key=lambda entry: entry.name)
    except ReviewBundleAccessError:
        raise
    except OSError as exc:
        raise ReviewBundleAccessError(
            f"Cannot inspect review bundle {directory}: {exc}"
        ) from exc

    entry_names = {entry.name for entry in entries}
    missing = sorted(_REVIEW_BUNDLE_FILENAMES - entry_names)
    unexpected = sorted(entry_names - _REVIEW_BUNDLE_FILENAMES)
    if missing or unexpected:
        details = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if unexpected:
            details.append("unexpected " + ", ".join(unexpected))
        _add_finding(
            findings,
            "GTTAB001",
            ".",
            "File set does not match the contract: " + "; ".join(details),
        )

    contents: dict[str, bytes] = {}
    for entry in entries:
        if entry.is_symlink() or not entry.is_file():
            _add_finding(
                findings,
                "GTTAB002",
                entry.name,
                "Bundle entries must be regular files, not links or directories",
            )
            continue
        if entry.name not in _REVIEW_BUNDLE_FILENAMES:
            continue
        try:
            contents[entry.name] = entry.read_bytes()
        except OSError as exc:
            raise ReviewBundleAccessError(
                f"Cannot read review bundle file {entry}: {exc}"
            ) from exc

    for name in ("memo.md", "verification.md", "review.html"):
        if name not in contents:
            continue
        try:
            contents[name].decode("utf-8")
        except UnicodeDecodeError as exc:
            _add_finding(
                findings,
                "GTTAB007",
                name,
                f"Text output must be UTF-8: {exc}",
            )

    manifest = None
    if "manifest.json" in contents:
        manifest = _parse_json_object(
            contents["manifest.json"],
            path="manifest.json",
            label="manifest",
            rule_id="GTTAB003",
            findings=findings,
        )
    bundle_interface = (
        str(manifest.get("interface"))
        if manifest is not None and manifest.get("interface") is not None
        else None
    )
    if manifest is not None:
        if manifest.get("interface") != REVIEW_BUNDLE_VERSION:
            _add_finding(
                findings,
                "GTTAB004",
                "manifest.json#/interface",
                f"interface must be {REVIEW_BUNDLE_VERSION}",
            )
        scalar_expectations = {
            "verification_interface": MEMO_VERIFICATION_VERSION,
            "human_review_required": True,
        }
        for field, expected in scalar_expectations.items():
            if manifest.get(field) != expected:
                _add_finding(
                    findings,
                    "GTTAB005",
                    f"manifest.json#/{field}",
                    f"{field} must be {expected!r}",
                )
        for field in ("strict", "passed"):
            if type(manifest.get(field)) is not bool:
                _add_finding(
                    findings,
                    "GTTAB005",
                    f"manifest.json#/{field}",
                    f"{field} must be a boolean",
                )
        if not isinstance(manifest.get("packet_status"), str) or not manifest.get(
            "packet_status"
        ):
            _add_finding(
                findings,
                "GTTAB005",
                "manifest.json#/packet_status",
                "packet_status must be a non-empty string",
            )
        if not isinstance(manifest.get("limitations"), str) or not manifest.get(
            "limitations"
        ):
            _add_finding(
                findings,
                "GTTAB005",
                "manifest.json#/limitations",
                "limitations must be a non-empty string",
            )
        _check_input_manifest(manifest, findings)
        _check_output_manifest(manifest, contents, findings)

    receipt = None
    if "verification.json" in contents:
        receipt = _parse_json_object(
            contents["verification.json"],
            path="verification.json",
            label="verification receipt",
            rule_id="GTTAB009",
            findings=findings,
        )
    if receipt is not None:
        _check_receipt(receipt, manifest, findings)
    verification_passed = (
        receipt.get("passed")
        if receipt is not None and type(receipt.get("passed")) is bool
        else None
    )
    packet_status = (
        receipt.get("packet_status")
        if receipt is not None and isinstance(receipt.get("packet_status"), str)
        else None
    )

    if "verification.sarif" in contents:
        sarif = _parse_json_object(
            contents["verification.sarif"],
            path="verification.sarif",
            label="SARIF",
            rule_id="GTTAB011",
            findings=findings,
        )
        if sarif is not None:
            if sarif.get("version") != "2.1.0" or not isinstance(
                sarif.get("runs"), list
            ):
                _add_finding(
                    findings,
                    "GTTAB011",
                    "verification.sarif",
                    "SARIF must declare version 2.1.0 and a runs array",
                )

    if "repair.md" in contents and receipt is not None:
        try:
            repair = contents["repair.md"].decode("utf-8")
        except UnicodeDecodeError as exc:
            _add_finding(
                findings,
                "GTTAB012",
                "repair.md",
                f"repair.md must be UTF-8: {exc}",
            )
        else:
            packet_status = receipt.get("packet_status")
            gtta_findings = receipt.get("gtta_findings")
            repair_complete = (
                packet_status == "packet_complete"
                and isinstance(gtta_findings, list)
                and not gtta_findings
            )
            expected_heading = (
                "# GTTA Memo Repair Status: Complete"
                if repair_complete
                else "# GTTA Memo Repair Instructions"
            )
            if not repair.startswith(expected_heading):
                _add_finding(
                    findings,
                    "GTTAB012",
                    "repair.md",
                    "Repair status disagrees with verification.json",
                )

    return ReviewBundleCheckReport(
        bundle_dir=directory,
        bundle_interface=bundle_interface,
        verification_passed=verification_passed,
        packet_status=packet_status,
        findings=tuple(findings),
    )
