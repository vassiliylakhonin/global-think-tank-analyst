"""MCP adapter for the packaged analytical method."""

try:
    from mcp.server import MCPServer
except ImportError as exc:  # pragma: no cover - exercised by installation users
    raise ImportError(
        "MCP support is optional. Install global-think-tank-analyst[mcp]."
    ) from exc

from . import __version__
from .discipline import check_contract
from .resources import get_mode_template as load_mode_template
from .resources import get_skill_prompt as load_skill_prompt


app = MCPServer(
    name="global-think-tank-analyst",
    version=__version__,
    instructions=(
        "Provides the Policy Risk Memo Architect method and a versioned "
        "method-contract preflight. It does not verify factual claims or sources."
    ),
)


@app.tool()
async def get_skill_prompt(language: str = "en") -> str:
    """Return the complete packaged analyst instructions in English or Russian."""
    return load_skill_prompt(language)


@app.tool()
async def get_mode_template(mode: str, language: str = "en") -> str:
    """Return the canonical section for a specific memo mode.

    Args:
        mode: Mode A, B, C, D, E, F, or G
    """
    return load_mode_template(mode, language)


@app.tool()
async def check_memo_contract(
    draft: str, mode: str | None = None
) -> dict[str, object]:
    """Run the versioned method-contract preflight on a draft memo.

    This check does not verify claim/source support, factuality, or analytical
    quality. Use Agenda Intelligence MD for evidence-packet linting.

    Args:
        draft: The markdown text of the draft memo.
    """
    return check_contract(draft, mode=mode).to_dict()


if __name__ == "__main__":
    app.run()
