"""Load the packaged analytical method through one stable interface."""

from importlib.resources import files


class SkillResourceError(RuntimeError):
    """Raised when the installed package is missing its analytical method."""


_LANGUAGE_ALIASES = {
    "en": "SKILL.md",
    "english": "SKILL.md",
    "ru": "SKILL_RU.md",
    "russian": "SKILL_RU.md",
}


def get_skill_prompt(language: str = "en") -> str:
    """Return the packaged analytical instructions for ``language``.

    The method is product-critical package data. Missing or unreadable data is
    therefore a hard failure rather than a reason to return a generic prompt.
    """
    normalized = language.strip().lower()
    try:
        filename = _LANGUAGE_ALIASES[normalized]
    except KeyError as exc:
        supported = ", ".join(sorted(_LANGUAGE_ALIASES))
        raise ValueError(
            f"Unsupported language {language!r}. Supported values: {supported}."
        ) from exc

    resource = files("gtta.skills").joinpath(filename)
    try:
        prompt = resource.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError) as exc:
        raise SkillResourceError(
            f"Required packaged skill resource {filename!r} is unavailable. "
            "Reinstall global-think-tank-analyst from a complete distribution."
        ) from exc

    if not prompt.strip():
        raise SkillResourceError(
            f"Required packaged skill resource {filename!r} is empty."
        )
    return prompt


def get_mode_template(mode: str, language: str = "en") -> str:
    """Return the canonical memo-mode section from the packaged method."""
    normalized = mode.strip().upper().removeprefix("MODE ")
    if normalized not in set("ABCDEFG"):
        raise ValueError("Memo mode must be one of A, B, C, D, E, F, or G.")

    prompt = get_skill_prompt(language)
    marker = f"### Mode {normalized} "
    start = prompt.find(marker)
    if start == -1:
        raise SkillResourceError(
            f"Mode {normalized} is not defined in the packaged {language!r} skill."
        )
    following = start + len(marker)
    candidates = (
        prompt.find("\n### Mode ", following),
        prompt.find("\n## ", following),
    )
    ends = [position for position in candidates if position != -1]
    end = min(ends) if ends else None
    return prompt[start:end].strip()
