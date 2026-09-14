"""Build two verified review bundles as one atomic developer release."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
import uuid
import zipfile
from pathlib import Path
from typing import Any

from gtta.review import build_review_bundle, check_review_bundle


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CASES = (
    "kazakhstan-crma-flagship",
    "middle-corridor-sanctions-flagship",
)
BUNDLE_FILENAMES = (
    "manifest.json",
    "memo.md",
    "repair.md",
    "review.html",
    "verification.json",
    "verification.md",
    "verification.sarif",
)
FIXED_ZIP_TIME = (2026, 9, 14, 0, 0, 0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "artifacts" / "flagship-portfolio",
        help="Complete release directory to replace after every case passes.",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def write_bundle_zip(bundle_dir: Path, case_id: str, output: Path) -> None:
    actual = {path.name for path in bundle_dir.iterdir() if path.is_file()}
    if actual != set(BUNDLE_FILENAMES):
        raise RuntimeError(
            f"{case_id}: review bundle contract mismatch; found {sorted(actual)}"
        )
    archive_root = f"{case_id}-review-bundle"
    with zipfile.ZipFile(
        output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for filename in BUNDLE_FILENAMES:
            info = zipfile.ZipInfo(
                f"{archive_root}/{filename}", date_time=FIXED_ZIP_TIME
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (bundle_dir / filename).read_bytes())
    with zipfile.ZipFile(output) as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise RuntimeError(f"{case_id}: corrupt ZIP member {bad_member}")


def build_release(staging: Path) -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    for case_id in CASES:
        case_dir = HERE / "cases" / case_id
        bundle_dir = staging / case_id / "review-bundle"
        result = build_review_bundle(
            case_dir / "memo.json",
            source_catalog_path=case_dir / "memo.sources.json",
            output_dir=bundle_dir,
            strict=True,
        )
        integrity = check_review_bundle(bundle_dir)
        if (
            not result.report.passed
            or result.report.packet_status != "packet_complete"
        ):
            raise RuntimeError(f"{case_id}: strict verification requires review")
        if not integrity.passed:
            raise RuntimeError(f"{case_id}: review-bundle integrity check failed")

        zip_path = staging / f"{case_id}-review-bundle.zip"
        write_bundle_zip(bundle_dir, case_id, zip_path)
        cases.append(
            {
                "case_id": case_id,
                "artifact_id": result.manifest["inputs"]["artifact"][
                    "artifact_id"
                ],
                "passed": True,
                "packet_status": result.report.packet_status,
                "claim_count": len(result.report.packet.get("claims", [])),
                "source_count": len(result.report.packet.get("sources", [])),
                "human_review_required": True,
                "bundle_manifest_sha256": sha256_file(
                    bundle_dir / "manifest.json"
                ),
                "zip_sha256": sha256_file(zip_path),
            }
        )

    summary = {
        "schema_version": "gtta.flagship-portfolio@1.0",
        "evidence_mode": "live-source-backed",
        "passed": True,
        "case_count": len(cases),
        "claim_count": sum(item["claim_count"] for item in cases),
        "source_count": sum(item["source_count"] for item in cases),
        "cases": cases,
        "limitations": (
            "PASS establishes deterministic structural and lexical completeness, "
            "not factual truth, source authority, legal sufficiency, decision safety, "
            "or current sanctions status. Human review remains required."
        ),
    }
    write_json(staging / "summary.json", summary)
    return summary


def remove_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def promote(staging: Path, output: Path) -> None:
    backup = output.with_name(f".{output.name}.backup-{uuid.uuid4().hex}")
    had_previous = output.exists() or output.is_symlink()
    if had_previous:
        os.replace(output, backup)
    try:
        os.replace(staging, output)
    except Exception:
        if had_previous and backup.exists():
            os.replace(backup, output)
        raise
    if had_previous:
        remove_path(backup)


def main() -> int:
    args = parse_args()
    output = args.out.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=f".{output.name}.tmp-", dir=output.parent)
    )
    try:
        summary = build_release(staging)
        promote(staging, output)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise
    print(json.dumps({"output": str(output), **summary}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
