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
    
    draft = f"""# Draft Memo: {topic}
    
**Question:** {topic}
**Decision:** [what action depends on it]
**Audience:** [founder / operator / leadership]
**Time horizon:** [days / months / 1–3 years]
**Evidence mode:** reasoning-only

## Executive Takeaway
[Your takeaway here]

## Next Steps
Use the `gtta` package or your LLM to expand this draft according to Mode {mode} rules.
"""
    console.print(Markdown(draft))

if __name__ == "__main__":
    app()
