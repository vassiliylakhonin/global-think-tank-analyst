import asyncio
from pathlib import Path
try:
    from mcp.server.mcpserver import MCPServer
except ImportError:
    class MCPServer:  # type: ignore
        def __init__(self, name: str):
            self.name = name
        def tool(self):
            def decorator(fn):
                return fn
            return decorator
        def run(self):
            pass

app = MCPServer("global-think-tank-analyst")

@app.tool()
async def get_skill_prompt() -> str:
    """Returns the core SKILL.md instructions for the analyst."""
    skill_path = Path(__file__).parent.parent.parent / "SKILL.md"
    return skill_path.read_text(encoding="utf-8") if skill_path.exists() else "SKILL.md not found."

@app.tool()
async def get_mode_template(mode: str) -> str:
    """Returns the expected schema/template for a specific memo mode.
    
    Args:
        mode: Mode A, B, C, D, E, F, or G
    """
    return f"Template for Mode {mode} is requested. See SKILL.md for details."

@app.tool()
async def validate_memo_evidence(draft: str) -> str:
    """Checks a draft memo for evidence discipline violations (e.g. missing tags).
    
    Args:
        draft: The markdown text of the draft memo.
    """
    errors = []
    if "Evidence mode:" not in draft:
        errors.append("- Missing 'Evidence mode:' declaration.")
    if "Facts vs Assessments" not in draft and "## Quick assessment" not in draft:
        errors.append("- Missing explicit separation of facts and assessments.")
    if "[primary]" not in draft and "[secondary]" not in draft and "[user-provided]" not in draft:
        errors.append("- Missing Axis A provenance tags (e.g., [primary], [secondary]).")
    if "[inference]" not in draft and "[analyst-judgment]" not in draft:
        errors.append("- Missing analytical tags (e.g., [inference], [analyst-judgment]).")
        
    if not errors:
        return "✅ Validation passed. Evidence discipline appears to be followed."
    
    return "❌ Validation Failed. Please fix the following:\n" + "\n".join(errors)

if __name__ == "__main__":
    app.run()
