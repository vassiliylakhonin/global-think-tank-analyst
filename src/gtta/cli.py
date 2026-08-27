import typer
from rich.console import Console
from rich.markdown import Markdown

app = typer.Typer(help="Global Think Tank Analyst CLI")
console = Console()

@app.command()
def new(
    mode: str = typer.Option("B", help="Memo mode (A-G)"),
    topic: str = typer.Option(..., help="Topic or question")
):
    """Generate a draft memo structure."""
    console.print(f"[bold green]Generating a draft for Mode {mode} on topic:[/bold green] {topic}")
    draft = f"""# Draft Memo: {topic}\n\n**Question:** {topic}\n**Decision:** [what action depends on it]\n**Audience:** [founder / operator]\n**Time horizon:** [days / months / 1–3 years]\n**Evidence mode:** reasoning-only\n\n## Executive Takeaway\n[Your takeaway here]\n\n## Next Steps\nUse `gtta` to expand this draft."""
    console.print(Markdown(draft))

@app.command()
def ui():
    """Launch the interactive web UI (requires 'streamlit' extra)."""
    import os
    from pathlib import Path
    app_path = Path(__file__).parent / "app.py"
    console.print(f"[bold green]Starting Streamlit UI...[/bold green]")
    os.system(f"streamlit run {app_path}")

@app.command()
def server(host: str = "0.0.0.0", port: int = 8000):
    """Launch the Enterprise FastAPI Server (requires 'enterprise' extra)."""
    try:
        import uvicorn
        from .server import app as api_app
    except ImportError:
        console.print("[bold red]Error:[/bold red] FastAPI/Uvicorn not installed. Run: pip install global-think-tank-analyst[enterprise]")
        raise typer.Exit(1)
        
    console.print(f"[bold green]Starting Global Think Tank Analyst API on {host}:{port}...[/bold green]")
    uvicorn.run(api_app, host=host, port=port)

@app.command()
def ingest(file_path: str):
    """Ingest a heavy PDF document into the Analyst's local vector store (requires 'enterprise' extra)."""
    try:
        from langchain_community.document_loaders import PyPDFLoader
    except ImportError:
        console.print("[bold red]Error:[/bold red] PyPDF missing. Run: pip install global-think-tank-analyst[enterprise]")
        raise typer.Exit(1)
        
    console.print(f"[bold blue]Ingesting document:[/bold blue] {file_path}")
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    console.print(f"[bold green]Success![/bold green] Ingested {len(pages)} pages into local FAISS index (Simulated).")

if __name__ == "__main__":
    app()
