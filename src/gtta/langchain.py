from typing import Optional

from .skill import SkillNotAvailableError, compose_prompt, get_skill_prompt  # noqa: F401

try:
    from langchain_core.messages import SystemMessage
except ImportError:  # pragma: no cover - exercised only without the extra installed
    class SystemMessage:  # type: ignore
        def __init__(self, content: str):
            self.content = content


def get_system_prompt(
    language: str = "en", extra_instructions: Optional[str] = None
) -> SystemMessage:
    """Return the analytical method as a LangChain SystemMessage.

    Raises:
        SkillNotAvailableError: if the method is missing from the installed
            package. This deliberately does not fall back to a placeholder:
            a caller cannot tell a stub prompt from the real method until the
            output is already wrong.
    """
    return SystemMessage(content=compose_prompt(language, extra_instructions))
