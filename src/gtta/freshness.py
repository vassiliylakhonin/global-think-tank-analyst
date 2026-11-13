"""Calendar freshness from caller-supplied dates and TTLs, not confidence decay."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from .artifact import ClaimKind, MemoArtifactV2, check_memo_artifact


def evidence_age(payload: str | dict[str, Any], as_of: date) -> dict[str, Any]:
    report = check_memo_artifact(payload)
    if not report.passed or not isinstance(report.artifact, MemoArtifactV2):
        raise ValueError("evidence-age requires a valid gtta.memo@2.0 artifact")
    artifact = report.artifact
    claims = []
    stale_ids = set()
    for claim in artifact.claims:
        if claim.kind is not ClaimKind.FACT:
            continue
        row: dict[str, Any] = {
            "claim_id": claim.claim_id,
            "source_refs": claim.source_refs,
        }
        if claim.evidence_as_of is None or claim.valid_for_days is None:
            row["status"] = "unknown"
        else:
            expires_on = claim.evidence_as_of + timedelta(days=claim.valid_for_days)
            age = (as_of - claim.evidence_as_of).days
            row.update(
                evidence_as_of=claim.evidence_as_of.isoformat(),
                age_days=age,
                valid_for_days=claim.valid_for_days,
                expires_on=expires_on.isoformat(),
            )
            row["status"] = (
                "future-dated"
                if age < 0
                else "expired"
                if as_of >= expires_on
                else "within-declared-ttl"
            )
            if row["status"] == "expired":
                stale_ids.add(claim.claim_id)
        claims.append(row)

    # Include descendants that rely on stale facts. Cycles are already rejected by
    # the artifact contract. These are declared dependencies, not semantic links.
    affected = set(stale_ids)
    while True:
        expanded = affected | {
            c.claim_id for c in artifact.claims if set(c.basis_claim_ids) & affected
        }
        if expanded == affected:
            break
        affected = expanded
    blocks = {
        "bottom_line": artifact.bottom_line.claim_ids,
        **{
            f"sections.{key}": block.claim_ids
            for key, block in artifact.sections.items()
        },
        **{
            f"options.{option.option_id}": option.basis_claim_ids
            for option in artifact.options
        },
        **{
            f"indicators.{indicator.indicator_id}": indicator.basis_claim_ids
            for indicator in artifact.indicators
        },
    }
    affected_blocks = [
        {"path": key, "affected_claim_ids": sorted(set(ids) & affected)}
        for key, ids in blocks.items()
        if set(ids) & affected
    ]
    return {
        "schema_version": "gtta.evidence-age@1.0",
        "as_of": as_of.isoformat(),
        "facts": claims,
        "expired_fact_ids": sorted(stale_ids),
        "affected_claim_ids": sorted(affected),
        "affected_blocks": affected_blocks,
        "human_review_required": True,
        "limitations": "Calendar expiry from manually declared evidence dates and TTLs only. Unknown dates are not fresh. Within TTL does not mean true or current; no source retrieval, probability decay, monitoring or automatic action was performed.",
    }
