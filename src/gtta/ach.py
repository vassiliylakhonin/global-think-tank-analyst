"""ACH inconsistency counting from an explicitly supplied complete matrix."""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator


class ACHMatrix(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    schema_version: Literal["gtta.ach@1.0"] = "gtta.ach@1.0"
    hypotheses: list[str] = Field(min_length=2)
    evidence: list[str] = Field(min_length=1)
    # Evidence ID -> hypothesis ID -> explicit assessment, supplied by a person.
    matrix: dict[
        str, dict[str, Literal["consistent", "inconsistent", "neutral", "unknown"]]
    ]

    @model_validator(mode="after")
    def complete(self):
        for label, values in (
            ("hypotheses", self.hypotheses),
            ("evidence", self.evidence),
        ):
            if any(not value for value in values) or len(set(values)) != len(values):
                raise ValueError(f"{label} IDs must be nonempty and unique")
        if set(self.matrix) != set(self.evidence):
            raise ValueError("matrix must contain exactly the evidence IDs")
        if any(set(row) != set(self.hypotheses) for row in self.matrix.values()):
            raise ValueError(
                "every evidence row must contain exactly all hypothesis IDs"
            )
        return self


def rank_ach(payload: str | dict) -> dict:
    matrix = (
        ACHMatrix.model_validate_json(payload)
        if isinstance(payload, str)
        else ACHMatrix.model_validate(payload)
    )
    results = []
    for hypothesis in matrix.hypotheses:
        cells = {
            evidence: matrix.matrix[evidence][hypothesis]
            for evidence in matrix.evidence
        }
        inconsistent = [key for key, value in cells.items() if value == "inconsistent"]
        unknown = [key for key, value in cells.items() if value == "unknown"]
        results.append(
            {
                "hypothesis_id": hypothesis,
                "inconsistencies": len(inconsistent),
                "inconsistent_evidence_ids": inconsistent,
                "unknown_count": len(unknown),
                "assessed_count": len(cells) - len(unknown),
            }
        )
    results.sort(key=lambda row: row["inconsistencies"])
    for row in results:
        row["rank"] = 1 + sum(
            other["inconsistencies"] < row["inconsistencies"] for other in results
        )
    return {
        "schema_version": "gtta.ach-result@1.0",
        "ranking": results,
        "evidence_count": len(matrix.evidence),
        "human_review_required": True,
        "limitations": "Counts supplied inconsistencies only. Ties share rank; unknown cells are reported, not evidence for a hypothesis. This does not estimate probability, establish truth, assess evidence independence or remove analyst bias.",
    }
