import typer
import os
import subprocess
import sys
from rich.console import Console
from rich.markdown import Markdown

app = typer.Typer(help="Global Think Tank Analyst CLI")
console = Console()


@app.command()
def new(
    mode: str = typer.Option("B", help="Memo mode (A-G)"),
    topic: str = typer.Option(..., help="Topic or question"),
):
    """Generate a draft memo structure."""
    console.print(
        f"[bold green]Generating a draft for Mode {mode} on topic:[/bold green] {topic}"
    )
    draft = f"""# Draft Memo: {topic}\n\n**Question:** {topic}\n**Decision:** [what action depends on it]\n**Audience:** [founder / operator]\n**Time horizon:** [days / months / 1–3 years]\n**Evidence mode:** reasoning-only\n\n## Executive Takeaway\n[Your takeaway here]\n\n## Next Steps\nUse `gtta` to expand this draft."""
    console.print(Markdown(draft))


@app.command()
def ui(host: str = "127.0.0.1", port: int = 8501):
    """Launch the interactive web UI (requires 'streamlit' extra)."""
    from pathlib import Path

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


@app.command()
def ingest(file_path: str):
    """Ingest a heavy PDF document into the Analyst's local vector store (requires 'enterprise' extra)."""
    try:
        from langchain_community.document_loaders import PyPDFLoader
    except ImportError:
        console.print(
            "[bold red]Error:[/bold red] PyPDF missing. Run: pip install global-think-tank-analyst[enterprise]"
        )
        raise typer.Exit(1)

    console.print(f"[bold blue]Ingesting document:[/bold blue] {file_path}")
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    console.print(
        f"[bold green]Parsed {len(pages)} pages.[/bold green] "
        "This command does not yet write a persistent vector index."
    )


@app.command()
def dark_factory():
    """Run the legacy experimental worker and queue its draft for review."""
    from pathlib import Path

    script = Path(__file__).parent.parent.parent / "scripts" / "dark_factory_worker.py"
    console.print("[bold]Starting experimental signal-draft worker...[/bold]")
    subprocess.run([sys.executable, str(script)], check=True)


if __name__ == "__main__":
    app()
