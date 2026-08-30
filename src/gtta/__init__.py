"""Global Think Tank Analyst Python package."""

from .artifact import (
    ARTIFACT_SCHEMA_VERSION,
    ArtifactFinding,
    ArtifactReport,
    ClaimKind,
    Confidence,
    DecisionOption,
    EvidenceMode,
    MemoArtifact,
    MemoClaim,
    MemoMode,
    NarrativeBlock,
    Provenance,
    WatchIndicator,
    check_memo_artifact,
    get_memo_artifact_schema,
    render_memo_artifact,
)
from .discipline import ContractReport, Finding, Severity, check_contract
from .resources import SkillResourceError, get_mode_template, get_skill_prompt


__version__ = "1.6.0.dev0"

__all__ = (
    "SkillResourceError",
    "ARTIFACT_SCHEMA_VERSION",
    "ArtifactFinding",
    "ArtifactReport",
    "ClaimKind",
    "Confidence",
    "DecisionOption",
    "EvidenceMode",
    "MemoArtifact",
    "MemoClaim",
    "MemoMode",
    "NarrativeBlock",
    "Provenance",
    "WatchIndicator",
    "ContractReport",
    "Finding",
    "Severity",
    "check_contract",
    "check_memo_artifact",
    "get_memo_artifact_schema",
    "get_mode_template",
    "get_skill_prompt",
    "render_memo_artifact",
)
