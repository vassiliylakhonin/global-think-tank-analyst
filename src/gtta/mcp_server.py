import asyncio
import os
from pathlib import Path

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.types as types
import mcp.server.stdio

app = Server("global-think-tank-analyst")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_skill_prompt",
            description="Returns the core SKILL.md instructions for the analyst.",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="get_mode_template",
            description="Returns the expected schema/template for a specific memo mode.",
            inputSchema={
                "type": "object",
                "properties": {
                    "mode": {"type": "string", "description": "Mode A, B, C, D, E, F, or G"}
                },
                "required": ["mode"]
            }
        ),
        types.Tool(
            name="validate_memo_evidence",
            description="Checks a draft memo for evidence discipline violations (e.g. missing tags).",
            inputSchema={
                "type": "object",
                "properties": {
                    "draft": {"type": "string", "description": "The markdown text of the draft memo."}
                },
                "required": ["draft"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "get_skill_prompt":
        skill_path = Path(__file__).parent.parent.parent / "SKILL.md"
        content = skill_path.read_text(encoding="utf-8") if skill_path.exists() else "SKILL.md not found."
        return [types.TextContent(type="text", text=content)]
    
    if name == "get_mode_template":
        mode = arguments.get("mode", "B")
        return [types.TextContent(type="text", text=f"Template for Mode {mode} is requested. See SKILL.md for details.")]
    
    if name == "validate_memo_evidence":
        draft = arguments.get("draft", "")
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
            return [types.TextContent(type="text", text="✅ Validation passed. Evidence discipline appears to be followed.")]
        
        report = "❌ Validation Failed. Please fix the following:\n" + "\n".join(errors)
        return [types.TextContent(type="text", text=report)]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="global-think-tank-analyst",
                server_version="1.4.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
