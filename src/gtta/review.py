"""Build one auditable review bundle from a source-backed MemoArtifact.

This module owns file orchestration only. Memo validation remains in
``gtta.artifact`` and claim/source checking plus review rendering remain at the
Agenda Intelligence seam exposed by ``gtta.verification``.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .artifact import MemoArtifact, check_memo_artifact, render_memo_artifact
from .sarif import render_verification_sarif
from .verification import (
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


class ReviewBundleInputError(ValueError):
    """The requested review bundle cannot be created safely."""


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
    media_types = {
        "memo.md": "text/markdown",
        "verification.json": "application/json",
        "verification.md": "text/markdown",
        "review.html": "text/html",
        "verification.sarif": "application/sarif+json",
        "repair.md": "text/markdown",
    }
    manifest: dict[str, Any] = {
        "interface": REVIEW_BUNDLE_VERSION,
        "verification_interface": receipt["interface"],
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
                "media_type": media_types[name],
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
