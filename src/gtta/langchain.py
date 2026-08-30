from typing import Optional

try:
    from langchain_core.messages import SystemMessage
except ImportError as exc:  # pragma: no cover - exercised by installation users
    raise ImportError(
        "LangChain support is optional. Install "
        "global-think-tank-analyst[langchain]."
    ) from exc

from .resources import get_skill_prompt

def get_system_prompt(language: str = "en", extra_instructions: Optional[str] = None) -> SystemMessage:
    """Returns the Global Think Tank Analyst SKILL.md as a LangChain SystemMessage."""
    prompt = get_skill_prompt(language)
    if extra_instructions:
        prompt += f"\n\n## Additional Context/Instructions\n{extra_instructions}"
    
    return SystemMessage(content=prompt)
