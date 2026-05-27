#!/usr/bin/env python3
"""Validate skill-improvement JSONL case files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = {
    "id",
    "skill",
    "split",
    "title",
    "prompt",
    "context",
    "expected_behaviors",
    "failure_modes",
    "scoring_notes",
}
ALLOWED_FIELDS = REQUIRED_FIELDS
ALLOWED_SPLITS = {"train", "val", "test"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def validate_case(case: dict, path: Path, line_no: int, seen_ids: set[str]) -> list[str]:
    errors: list[str] = []

    missing = sorted(REQUIRED_FIELDS - case.keys())
    if missing:
        errors.append(f"{path}:{line_no}: missing fields: {', '.join(missing)}")

    extra = sorted(set(case.keys()) - ALLOWED_FIELDS)
    if extra:
        errors.append(f"{path}:{line_no}: unknown fields: {', '.join(extra)}")

    case_id = case.get("id")
    if not isinstance(case_id, str) or not ID_RE.match(case_id):
        errors.append(f"{path}:{line_no}: id must be lowercase kebab-case")
    elif case_id in seen_ids:
        errors.append(f"{path}:{line_no}: duplicate id: {case_id}")
    else:
        seen_ids.add(case_id)

    if case.get("split") not in ALLOWED_SPLITS:
        errors.append(f"{path}:{line_no}: split must be one of {sorted(ALLOWED_SPLITS)}")

    for field in ("skill", "title", "prompt", "context", "scoring_notes"):
        if not isinstance(case.get(field), str) or not case.get(field, "").strip():
            errors.append(f"{path}:{line_no}: {field} must be a non-empty string")

    for field in ("expected_behaviors", "failure_modes"):
        value = case.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"{path}:{line_no}: {field} must be a non-empty list")
        elif not all(isinstance(item, str) and item.strip() for item in value):
            errors.append(f"{path}:{line_no}: {field} entries must be non-empty strings")

    return errors


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()

    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue

            try:
                case = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{path}:{line_no}: invalid JSON: {exc.msg}")
                continue

            if not isinstance(case, dict):
                errors.append(f"{path}:{line_no}: case must be a JSON object")
                continue

            errors.extend(validate_case(case, path, line_no, seen_ids))

    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: validate_cases.py CASE_FILE [CASE_FILE ...]", file=sys.stderr)
        return 2

    all_errors: list[str] = []
    for raw_path in argv[1:]:
        path = Path(raw_path)
        if not path.exists():
            all_errors.append(f"{path}: file does not exist")
            continue
        all_errors.extend(validate_file(path))

    if all_errors:
        print("\n".join(all_errors), file=sys.stderr)
        return 1

    print(f"OK: validated {len(argv) - 1} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
