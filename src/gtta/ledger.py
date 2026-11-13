"""Manual CSV ledger writes. No forecast generation or automatic resolution."""

from __future__ import annotations

import csv
import os
import tempfile
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .forecasts import load

COLUMNS = [
    "id",
    "logged_on",
    "claim",
    "probability",
    "resolve_by",
    "resolution_rule",
    "memo_ref",
    "indicator",
    "outcome",
    "resolved_on",
    "notes",
]


class ForecastEntry(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    id: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
    logged_on: date
    claim: str = Field(min_length=1)
    probability: int = Field(ge=1, le=99, strict=True)
    resolve_by: date
    resolution_rule: str = Field(min_length=1)
    memo_ref: str = ""
    indicator: str = ""
    outcome: Literal["", "yes", "no", "void"] = ""
    resolved_on: date | None = None
    notes: str = ""

    @model_validator(mode="after")
    def dates_and_outcome(self):
        if self.logged_on > self.resolve_by:
            raise ValueError("logged_on must not be after resolve_by")
        if bool(self.outcome) != (self.resolved_on is not None):
            raise ValueError("outcome and resolved_on must be supplied together")
        if self.resolved_on is not None and self.resolved_on < self.logged_on:
            raise ValueError("resolved_on must not precede logged_on")
        return self


def _validated_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = load(path)
    ids = set()
    for row in rows:
        parsed = dict(row)
        parsed["probability"] = int(row["probability"])
        parsed["resolved_on"] = row.get("resolved_on") or None
        entry = ForecastEntry.model_validate(parsed)
        if entry.id in ids:
            raise ValueError("duplicate existing forecast ID")
        ids.add(entry.id)
    return rows


@contextmanager
def _lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise ValueError("ledger path must not be a symlink")
    lock = path.with_name(path.name + ".lock")
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise ValueError(
            "ledger is locked; verify no writer is active before removing its .lock directory"
        ) from exc
    try:
        yield
    finally:
        lock.rmdir()


def _save(path: Path, rows: list[dict]):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=path.parent, delete=False
        ) as handle:
            temporary = Path(handle.name)
            writer = csv.DictWriter(handle, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def add_forecast(path: Path, payload: str | dict) -> dict:
    entry = (
        ForecastEntry.model_validate_json(payload)
        if isinstance(payload, str)
        else ForecastEntry.model_validate(payload)
    )
    if entry.outcome:
        raise ValueError(
            "new forecasts must be unresolved; use manual resolution later"
        )
    with _lock(path):
        rows = _validated_rows(path)
        if any(row["id"] == entry.id for row in rows):
            raise ValueError(
                "forecast ID already exists; immutable claims/probabilities cannot be overwritten"
            )
        row = entry.model_dump(mode="json")
        row["resolved_on"] = ""
        _save(path, [*rows, row])
    return {"id": entry.id, "status": "logged", "human_review_required": True}


def resolve_forecast(
    path: Path, forecast_id: str, outcome: str, resolved_on: date, source: str
) -> dict:
    if outcome not in {"yes", "no", "void"} or not source.strip():
        raise ValueError(
            "manual resolution needs yes/no/void and nonempty source or explanation"
        )
    with _lock(path):
        rows = _validated_rows(path)
        matches = [row for row in rows if row["id"] == forecast_id]
        if not matches:
            raise ValueError("forecast ID not found")
        row = matches[0]
        if row["outcome"]:
            raise ValueError(
                "forecast is already resolved; this command does not rewrite outcomes"
            )
        if resolved_on < date.fromisoformat(row["logged_on"]):
            raise ValueError("resolved_on must not precede logged_on")
        row["outcome"] = outcome
        row["resolved_on"] = resolved_on.isoformat()
        row["notes"] = (
            row.get("notes", "") + "\nManual resolution basis: " + source.strip()
        ).strip()
        _save(path, rows)
    return {
        "id": forecast_id,
        "status": "resolved",
        "outcome": outcome,
        "limitations": "The caller supplied the outcome and basis. No source retrieval or outcome verification was performed.",
    }
