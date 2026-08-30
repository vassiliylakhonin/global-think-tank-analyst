from typing import Optional

try:
    from llama_index.core.llms import ChatMessage, MessageRole
except ImportError as exc:  # pragma: no cover - exercised by installation users
    raise ImportError(
        "LlamaIndex support is optional. Install "
        "global-think-tank-analyst[llamaindex]."
    ) from exc

from .resources import get_skill_prompt

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
