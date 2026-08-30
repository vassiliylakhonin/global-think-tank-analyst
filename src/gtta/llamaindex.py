from enum import Enum
from typing import Any, List, Optional

from .skill import SkillNotAvailableError, compose_prompt, get_skill_prompt  # noqa: F401

try:
    from llama_index.core.llms import ChatMessage, MessageRole
except ImportError:  # pragma: no cover - exercised only without the extra installed
    class MessageRole(Enum):  # type: ignore
        SYSTEM = "system"
        USER = "user"
        ASSISTANT = "assistant"

    class ChatMessage:  # type: ignore
        def __init__(self, role: Any, content: str):
            self.role = role
            self.content = content


def get_system_message(
    language: str = "en", extra_instructions: Optional[str] = None
) -> ChatMessage:
    """Return the analytical method as a LlamaIndex system ChatMessage.

    Raises:
        SkillNotAvailableError: if the method is missing from the installed
            package. See ``gtta.skill`` for why this does not fall back.
    """
    return ChatMessage(
        role=MessageRole.SYSTEM,
        content=compose_prompt(language, extra_instructions),
    )


def get_chat_template(
    language: str = "en", extra_instructions: Optional[str] = None
) -> List[ChatMessage]:
    """Return a LlamaIndex message history seeded with the system prompt."""
    return [get_system_message(language, extra_instructions)]
