from pathlib import Path
from typing import Any, Optional

try:
    from langchain_core.messages import SystemMessage
except ImportError:
    class SystemMessage:  # type: ignore
        def __init__(self, content: str):
            self.content = content

def get_skill_prompt(language: str = "en") -> str:
    """Read the analytical skill instructions."""
    root = Path(__file__).parent.parent.parent
    filename = "SKILL_RU.md" if language.lower() in ("ru", "russian") else "SKILL.md"
    path = root / filename
    if not path.exists():
        return "You are a strategic-risk analyst."
    return path.read_text(encoding="utf-8")

def get_system_prompt(language: str = "en", extra_instructions: Optional[str] = None) -> SystemMessage:
    """Returns the Global Think Tank Analyst SKILL.md as a LangChain SystemMessage."""
    prompt = get_skill_prompt(language)
    if extra_instructions:
        prompt += f"\n\n## Additional Context/Instructions\n{extra_instructions}"
    
    return SystemMessage(content=prompt)
