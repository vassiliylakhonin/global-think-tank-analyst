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
    output_format: str = typer.Option(
        "text", "--format", help="Output format: text, json, or sarif"
    ),
    out: Optional[str] = typer.Option(None, help="Write output to this path"),
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

    selected_format = "json" if json_output else output_format.strip().lower()
    if selected_format not in {"text", "json", "sarif"}:
        console.print("[bold red]Error:[/bold red] format must be text, json, or sarif")
        raise typer.Exit(2)
    if json_output and output_format != "text":
        console.print("[bold red]Error:[/bold red] use either --json or --format")
        raise typer.Exit(2)

    if selected_format == "json":
        rendered = json.dumps(report.to_dict(), ensure_ascii=False, indent=2) + "\n"
    elif selected_format == "sarif":
        from .sarif import render_contract_sarif

        artifact_uri = "stdin" if file_path == "-" else Path(file_path).as_posix()
        rendered = (
            json.dumps(
                render_contract_sarif(report, artifact_uri=artifact_uri),
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )
    else:
        rendered = report.render_text() + "\n"
    if out:
        try:
            Path(out).write_text(rendered, encoding="utf-8")
        except OSError as exc:
            console.print(f"[bold red]Error:[/bold red] {exc}")
            raise typer.Exit(2)
        console.print(f"Wrote {out}", markup=False)
    else:
        typer.echo(rendered, nl=False)
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


@app.command(name="source-catalog-schema")
def source_catalog_schema_command():
    """Print the memo verification source-catalog JSON Schema."""

    from .verification import get_memo_source_catalog_schema

    console.print_json(
        json.dumps(get_memo_source_catalog_schema(), ensure_ascii=False)
    )


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


@app.command(name="verify")
def verify_command(
    file_path: str = typer.Argument(..., help="MemoArtifact JSON path, or '-' for stdin"),
    sources: Optional[str] = typer.Option(
        None,
        "--sources",
        help="Source catalog path; defaults to <memo>.sources.json when present",
    ),
    strict: bool = typer.Option(
        False, help="Exit 1 unless Agenda reports a complete packet and GTTA preflight is clean"
    ),
    output_format: str = typer.Option(
        "text", "--format", help="Output format: text, json, markdown, html, or sarif"
    ),
    out: Optional[str] = typer.Option(None, help="Write output to this path"),
    repair_prompt: Optional[str] = typer.Option(
        None,
        "--repair-prompt",
        help="Write bounded self-repair instructions to this Markdown path",
    ),
):
    """Project a MemoArtifact into Agenda Intelligence and check its evidence."""

    from .verification import (
        VerificationDependencyError,
        VerificationInputError,
        MemoSourceCatalog,
        SOURCE_CATALOG_VERSION,
        load_source_catalog,
        render_memo_repair_prompt,
        render_verification_html,
        render_verification_markdown,
        verify_memo_artifact,
    )

    selected_format = output_format.strip().lower()
    if selected_format not in {"text", "json", "markdown", "html", "sarif"}:
        console.print(
            "[bold red]Error:[/bold red] format must be text, json, markdown, html, or sarif"
        )
        raise typer.Exit(2)
    try:
        payload = sys.stdin.read() if file_path == "-" else Path(file_path).read_text(
            encoding="utf-8"
        )
    except OSError as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(2)

    artifact_report = check_memo_artifact(payload)
    if not artifact_report.passed or artifact_report.artifact is None:
        for finding in artifact_report.findings:
            console.print(
                f"[bold red]{finding.code}[/bold red] {finding.path}: "
                f"{finding.message}"
            )
        raise typer.Exit(1)

    try:
        artifact_path = None if file_path == "-" else Path(file_path).resolve()
        catalog_path = Path(sources).resolve() if sources else None
        if catalog_path is None and artifact_path is not None:
            candidate = artifact_path.with_name(
                artifact_path.stem + ".sources.json"
            )
            if candidate.is_file():
                catalog_path = candidate
        if catalog_path is not None:
            catalog = load_source_catalog(catalog_path.read_text(encoding="utf-8"))
            base_dir = catalog_path.parent
        else:
            catalog = MemoSourceCatalog(schema_version=SOURCE_CATALOG_VERSION)
            base_dir = artifact_path.parent if artifact_path is not None else Path.cwd()
        report = verify_memo_artifact(
            artifact_report.artifact,
            source_catalog=catalog,
            base_dir=base_dir,
            strict=strict,
        )
        if selected_format == "json":
            rendered = json.dumps(report.to_dict(), ensure_ascii=False, indent=2) + "\n"
        elif selected_format == "markdown":
            rendered = render_verification_markdown(report)
        elif selected_format == "html":
            rendered = render_verification_html(report)
        elif selected_format == "sarif":
            from .sarif import render_verification_sarif

            artifact_uri = "stdin" if file_path == "-" else Path(file_path).as_posix()
            rendered = (
                json.dumps(
                    render_verification_sarif(
                        report,
                        artifact_uri=artifact_uri,
                        artifact_text=payload,
                    ),
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n"
            )
        else:
            rendered = report.render_text() + "\n"
        repair_rendered = (
            render_memo_repair_prompt(report) if repair_prompt is not None else None
        )
    except (OSError, VerificationDependencyError, VerificationInputError) as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(2)

    if out and repair_prompt and Path(out).resolve() == Path(repair_prompt).resolve():
        console.print(
            "[bold red]Error:[/bold red] --out and --repair-prompt must use different paths"
        )
        raise typer.Exit(2)

    if out:
        try:
            Path(out).write_text(rendered, encoding="utf-8")
        except OSError as exc:
            console.print(f"[bold red]Error:[/bold red] {exc}")
            raise typer.Exit(2)
        console.print(f"Wrote {out}", markup=False)
    else:
        typer.echo(rendered, nl=False)
    if repair_prompt and repair_rendered is not None:
        try:
            Path(repair_prompt).write_text(repair_rendered, encoding="utf-8")
        except OSError as exc:
            console.print(f"[bold red]Error:[/bold red] {exc}")
            raise typer.Exit(2)
        console.print(f"Wrote {repair_prompt}", markup=False)
    if not report.passed:
        raise typer.Exit(1)


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
