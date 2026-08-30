"""Canonical loader for the analytical method.

The method text is the product. Earlier versions read it from the repository
root with ``Path(__file__).parent.parent.parent``, which resolves to a path
that does not exist in an installed package — and then returned the string
``"You are a strategic-risk analyst."`` when the file was missing. Every
``pip install`` therefore produced an agent that silently ran on a 33-character
stub instead of the method, with no error to notice.

Two rules follow, and both matter more than they look:

1. The method ships *inside* the package (``gtta/skills/``), so an installed
   copy carries it.
2. A missing method raises. A prompt builder that degrades quietly is worse
   than one that fails, because the caller cannot tell the difference between
   a loaded method and a stub until the output is already wrong.
"""

from pathlib import Path
from typing import Optional

SKILLS_DIR = Path(__file__).resolve().parent / "skills"

_FILENAMES = {
    "en": "SKILL.md",
    "ru": "SKILL_RU.md",
}

# The failure this guard exists for is a 33-character placeholder standing in
# for a 25,000-character method. The floor is set to catch a stub or a badly
# truncated file, not a subtly incomplete one; it is deliberately far below the
# shortest real variant so that editing the method never trips it spuriously.
MINIMUM_METHOD_LENGTH = 2000


class SkillNotAvailableError(RuntimeError):
    """The analytical method could not be loaded from the installed package."""


def resolve_language(language: str) -> str:
    return "ru" if language.lower() in ("ru", "russian") else "en"


def skill_path(language: str = "en") -> Path:
    return SKILLS_DIR / _FILENAMES[resolve_language(language)]


def get_skill_prompt(language: str = "en") -> str:
    """Return the canonical method text, or raise.

    Raises:
        SkillNotAvailableError: if the method is missing from the installed
            package or is too short to be the real document.
    """
    path = skill_path(language)
    if not path.exists():
        raise SkillNotAvailableError(
            f"The analytical method is missing from the installed package: {path}. "
            "This usually means the wheel was built without `gtta/skills/*.md` "
            "package data. Reinstall from a correctly built distribution; do not "
            "fall back to a placeholder prompt."
        )

    text = path.read_text(encoding="utf-8")
    if len(text) < MINIMUM_METHOD_LENGTH:
        raise SkillNotAvailableError(
            f"{path} is {len(text)} characters, below the {MINIMUM_METHOD_LENGTH}-character "
            "floor for the analytical method. A truncated method is not a usable one."
        )
    return text


def compose_prompt(language: str = "en", extra_instructions: Optional[str] = None) -> str:
    """Return the method text with optional caller instructions appended."""
    prompt = get_skill_prompt(language)
    if extra_instructions:
        prompt += f"\n\n## Additional Context/Instructions\n{extra_instructions}"
    return prompt
