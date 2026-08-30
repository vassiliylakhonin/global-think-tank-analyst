"""Global Think Tank Analyst Python package."""

from .discipline import ContractReport, Finding, Severity, check_contract
from .resources import SkillResourceError, get_mode_template, get_skill_prompt


__version__ = "1.5.0.dev0"

__all__ = (
    "SkillResourceError",
    "ContractReport",
    "Finding",
    "Severity",
    "check_contract",
    "get_mode_template",
    "get_skill_prompt",
)
