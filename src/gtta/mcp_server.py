"""MCP server exposing the analytical method and a memo discipline check."""

from mcp.server.mcpserver import MCPServer

from .skill import get_skill_prompt as _load_skill

app = MCPServer("global-think-tank-analyst", version="1.5.0")


@app.tool()
async def get_skill_prompt(language: str = "en") -> str:
    """Return the canonical analytical method.

    Args:
        language: "en" or "ru".
    """
    # Loaded from the installed package; raises rather than returning a stub,
    # because an agent cannot tell a placeholder prompt from the real method.
    return _load_skill(language)

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

def main() -> None:
    """Console-script entry point declared in pyproject.toml."""
    app.run(transport="stdio")


if __name__ == "__main__":
    main()
