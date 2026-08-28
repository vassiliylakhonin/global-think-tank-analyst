from enum import Enum
from pathlib import Path
from typing import Any, Optional

try:
    from llama_index.core.llms import ChatMessage, MessageRole
except ImportError:
    class MessageRole(Enum):  # type: ignore
        SYSTEM = "system"
        USER = "user"
        ASSISTANT = "assistant"

    class ChatMessage:  # type: ignore
        def __init__(self, role: Any, content: str):
            self.role = role
            self.content = content

def get_skill_prompt(language: str = "en") -> str:
    """Read the analytical skill instructions."""
    root = Path(__file__).parent.parent.parent
    filename = "SKILL_RU.md" if language.lower() in ("ru", "russian") else "SKILL.md"
    path = root / filename
    if not path.exists():
        return "You are a strategic-risk analyst."
    return path.read_text(encoding="utf-8")

def get_system_message(language: str = "en", extra_instructions: Optional[str] = None) -> ChatMessage:
    """
    Get the LlamaIndex ChatMessage (System) populated with the Global Think Tank Analyst prompt.
    """
    prompt = get_skill_prompt(language)
    if extra_instructions:
        prompt += f"\n\n## Additional Context/Instructions\n{extra_instructions}"
    
    return ChatMessage(
        role=MessageRole.SYSTEM,
        content=prompt
    )

def get_chat_template(language: str = "en", extra_instructions: Optional[str] = None) -> list[ChatMessage]:
    """
    Get a ready-to-use LlamaIndex message history with the system prompt initialized.
    """
    return [get_system_message(language, extra_instructions)]
