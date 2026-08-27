from langchain_core.messages import SystemMessage
import pathlib

def get_system_prompt() -> SystemMessage:
    """Returns the Global Think Tank Analyst SKILL.md as a LangChain SystemMessage."""
    skill_path = pathlib.Path(__file__).parent.parent.parent / "SKILL.md"
    if not skill_path.exists():
        return SystemMessage(content="You are Global Think Tank Analyst. Use structured memo formats.")
    
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return SystemMessage(content=content)
