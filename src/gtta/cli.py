import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown

from .artifact import (
    check_memo_artifact,
    get_memo_artifact_schema,
    render_memo_artifact,
)
from .discipline import check_contract
from .resources import get_mode_template

app = typer.Typer(help="Global Think Tank Analyst CLI")
console = Console()


@app.command()
def new(
    mode: str = typer.Option("B", help="Memo mode (A-G)"),
    topic: str = typer.Option(..., help="Topic or question"),
):
    """Generate a draft memo structure."""
    mode = mode.strip().upper()
    if mode not in set("ABCDEFG"):
        console.print("[bold red]Error:[/bold red] mode must be one of A-G.")
        raise typer.Exit(2)
    console.print(
        f"[bold green]Generating a draft for Mode {mode} on topic:[/bold green] {topic}"
    )
    mode_contract = get_mode_template(mode)
    draft = f"""# Draft Memo: {topic}\n\n**Question:** {topic}\n**Decision:** [what action depends on it]\n**Audience:** [founder / operator]\n**Time horizon:** [days / months / 1–3 years]\n**Evidence mode:** reasoning-only\n\n## Mode contract\n\n{mode_contract}\n\n## Draft\n\n[Complete the requested sections above. Human review required.]"""
    console.print(Markdown(draft))


@app.command(name="check-contract")
def check_contract_command(
    file_path: str = typer.Argument(..., help="Markdown memo path, or '-' for stdin"),
    mode: Optional[str] = typer.Option(None, help="Expected memo mode (A-G)"),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON"),
):
    """Check deterministic Policy Risk Memo Architect requirements."""
    try:
        text = sys.stdin.read() if file_path == "-" else Path(file_path).read_text(
            encoding="utf-8"
        )
        report = check_contract(text, mode=mode)
    except (OSError, ValueError) as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(2)

    if json_output:
        console.print_json(json.dumps(report.to_dict(), ensure_ascii=False))
    else:
        console.print(report.render_text(), markup=False)
    if not report.passed:
        raise typer.Exit(1)


@app.command(name="artifact-schema")
def artifact_schema_command():
    """Print the canonical MemoArtifact JSON Schema."""
    console.print_json(
        json.dumps(get_memo_artifact_schema(), ensure_ascii=False)
    )


@app.command(name="check-artifact")
def check_artifact_command(
    file_path: str = typer.Argument(..., help="MemoArtifact JSON path, or '-' for stdin"),
    json_output: bool = typer.Option(False, "--json", help="Emit structured JSON"),
):
    """Validate a structured memo artifact and its claim ledger."""
    try:
        payload = sys.stdin.read() if file_path == "-" else Path(file_path).read_text(
            encoding="utf-8"
        )
    except OSError as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(2)

    report = check_memo_artifact(payload)
    if json_output:
        console.print_json(json.dumps(report.to_dict(), ensure_ascii=False))
    elif report.passed:
        console.print(
            f"MemoArtifact: PASS ({report.to_dict()['schema_version']})",
            markup=False,
        )
    else:
        console.print("MemoArtifact: FAIL", markup=False)
        for finding in report.findings:
            console.print(
                f"- {finding.code} {finding.path}: {finding.message}", markup=False
            )
    if not report.passed:
        raise typer.Exit(1)


@app.command(name="render-artifact")
def render_artifact_command(
    file_path: str = typer.Argument(..., help="MemoArtifact JSON path, or '-' for stdin"),
):
    """Render a validated MemoArtifact as a human-readable Markdown memo."""
    try:
        payload = sys.stdin.read() if file_path == "-" else Path(file_path).read_text(
            encoding="utf-8"
        )
    except OSError as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(2)

    report = check_memo_artifact(payload)
    if not report.passed or report.artifact is None:
        for finding in report.findings:
            console.print(
                f"[bold red]{finding.code}[/bold red] {finding.path}: "
                f"{finding.message}"
            )
        raise typer.Exit(1)
    # Preserve exact Markdown when redirected to a file; Rich would hard-wrap it.
    typer.echo(render_memo_artifact(report.artifact), nl=False)


@app.command()
def ui(host: str = "127.0.0.1", port: int = 8501):
    """Launch the interactive web UI (requires 'streamlit' extra)."""
    app_path = Path(__file__).parent / "app.py"
    console.print(f"[bold green]Starting Streamlit UI on {host}:{port}...[/bold green]")
    subprocess.run(
        [
            "streamlit",
            "run",
            str(app_path),
            "--server.address",
            host,
            "--server.port",
            str(port),
        ],
        check=True,
    )


@app.command()
def server(host: str = "127.0.0.1", port: int = 8000):
    """Launch the experimental FastAPI server (requires 'enterprise' extra)."""
    try:
        import uvicorn
        from .server import app as api_app
    except ImportError:
        console.print(
            "[bold red]Error:[/bold red] FastAPI/Uvicorn not installed. Run: pip install global-think-tank-analyst[enterprise]"
        )
        raise typer.Exit(1)

    if host not in {"127.0.0.1", "localhost", "::1"} and not os.getenv("GTTA_API_KEY"):
        console.print(
            "[bold red]Refusing external bind without GTTA_API_KEY.[/bold red] "
            "Set a strong bearer key first."
        )
        raise typer.Exit(2)

    console.print(
        f"[bold green]Starting Global Think Tank Analyst API on {host}:{port}...[/bold green]"
    )
    uvicorn.run(api_app, host=host, port=port)


@app.command(name="parse-pdf")
def parse_pdf(file_path: str):
    """Parse a PDF and report its page count; no index is created."""
    try:
        from pypdf import PdfReader
    except ImportError:
        console.print(
            "[bold red]Error:[/bold red] pypdf missing. Install "
            "global-think-tank-analyst[enterprise]."
        )
        raise typer.Exit(1)

    console.print(f"[bold blue]Parsing document:[/bold blue] {file_path}")
    reader = PdfReader(file_path)
    console.print(
        f"[bold green]Parsed {len(reader.pages)} pages.[/bold green] "
        "No vector index was created."
    )


@app.command(name="mcp")
def mcp_server():
    """Run the MCP server over stdio (requires the 'mcp' extra)."""
    try:
        from .mcp_server import app as server_app
    except ImportError:
        console.print(
            "[bold red]Error:[/bold red] MCP support is not installed. Install "
            "global-think-tank-analyst[mcp]."
        )
        raise typer.Exit(1)
    server_app.run(transport="stdio")


if __name__ == "__main__":
    app()
