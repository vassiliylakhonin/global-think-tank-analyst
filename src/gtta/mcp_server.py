"""MCP adapter for the packaged analytical method."""

try:
    from mcp.server import MCPServer
except ImportError as exc:  # pragma: no cover - exercised by installation users
    raise ImportError(
        "MCP support is optional. Install global-think-tank-analyst[mcp]."
    ) from exc

from . import __version__
from .artifact import check_memo_artifact as validate_memo_artifact
from .artifact import get_memo_artifact_schema as load_memo_artifact_schema
from .artifact import render_memo_artifact as render_validated_artifact
from .discipline import check_contract
from .resources import get_mode_template as load_mode_template
from .resources import get_skill_prompt as load_skill_prompt


app = MCPServer(
    name="global-think-tank-analyst",
    version=__version__,
    instructions=(
        "Provides the Policy Risk Memo Architect method and a versioned "
        "method-contract preflight plus a structured MemoArtifact interface. "
        "It does not verify factual claims or sources."
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


@app.tool()
async def get_memo_artifact_schema() -> dict[str, object]:
    """Return the canonical JSON Schema for a structured memo artifact."""
    return load_memo_artifact_schema()


@app.tool()
async def check_memo_artifact(artifact: str) -> dict[str, object]:
    """Validate MemoArtifact JSON, including per-claim provenance structure.

    This check validates declarations and cross-references, not the truth or
    adequacy of the named sources.

    Args:
        artifact: A complete MemoArtifact JSON object encoded as a string.
    """
    return validate_memo_artifact(artifact).to_dict()


@app.tool()
async def render_memo_artifact(artifact: str) -> str:
    """Validate MemoArtifact JSON and render its canonical Markdown view.

    Args:
        artifact: A complete MemoArtifact JSON object encoded as a string.
    """
    report = validate_memo_artifact(artifact)
    if not report.passed or report.artifact is None:
        details = "; ".join(
            f"{finding.path}: {finding.message}" for finding in report.findings
        )
        raise ValueError(f"Invalid MemoArtifact: {details}")
    return render_validated_artifact(report.artifact)


if __name__ == "__main__":
    app.run()
