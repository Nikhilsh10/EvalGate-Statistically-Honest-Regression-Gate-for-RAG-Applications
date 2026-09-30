"""EvalGate CLI — Typer-based command-line interface.

Commands:
    run     — Run a full evaluation against the target RAG app.
    noise   — Repeat baseline N times to measure run-to-run noise.
    gate    — Run the regression gate (exit code 0=pass, 1=fail).
    report  — Generate HTML/Markdown evaluation report.
    version — Print the EvalGate version.
"""

from typing import Optional

import typer
from rich.console import Console

from evalgate import __version__

app = typer.Typer(
    name="evalgate",
    help="Statistically honest regression gate for RAG applications.",
    add_completion=False,
)
console = Console()


@app.command()
def run(
    config: str = typer.Option("config.yaml", "--config", "-c", help="Path to config file."),
    eval_set: str = typer.Option(
        "data/eval_v1/eval.jsonl", "--eval-set", "-e", help="Path to eval set JSONL."
    ),
    output_dir: str = typer.Option("runs/latest", "--output", "-o", help="Output directory."),
    seed: int = typer.Option(42, "--seed", "-s", help="Random seed for reproducibility."),
) -> None:
    """Run a full evaluation against the target RAG app."""
    console.print(f"[bold green]EvalGate v{__version__}[/bold green]")
    console.print(f"Config: {config}")
    console.print(f"Eval set: {eval_set}")
    console.print(f"Output: {output_dir}")
    console.print(f"Seed: {seed}")
    console.print("[yellow]⚠ Evaluation runner not yet implemented (M3).[/yellow]")


@app.command()
def noise(
    repeats: int = typer.Option(5, "--repeats", "-n", help="Number of repeated runs."),
    config: str = typer.Option("config.yaml", "--config", "-c", help="Path to config file."),
) -> None:
    """Repeat baseline N times to measure run-to-run noise."""
    console.print(f"[bold green]EvalGate Noise Measurement[/bold green]")
    console.print(f"Repeats: {repeats}")
    console.print("[yellow]⚠ Noise measurement not yet implemented (M5).[/yellow]")


@app.command()
def gate(
    baseline: str = typer.Option(..., "--baseline", "-b", help="Path to baseline run JSON."),
    candidate: str = typer.Option(..., "--candidate", "-c", help="Path to candidate run JSON."),
    threshold: float = typer.Option(0.05, "--threshold", "-t", help="Significance threshold."),
) -> None:
    """Run the regression gate. Exit code 0=pass, 1=fail."""
    console.print(f"[bold green]EvalGate Regression Gate[/bold green]")
    console.print(f"Baseline: {baseline}")
    console.print(f"Candidate: {candidate}")
    console.print(f"Threshold: {threshold}")
    console.print("[yellow]⚠ Gate not yet implemented (M5).[/yellow]")


@app.command()
def report(
    run_dir: str = typer.Option("runs/latest", "--run-dir", "-r", help="Run directory."),
    format: str = typer.Option("html", "--format", "-f", help="Output format: html or markdown."),
) -> None:
    """Generate HTML/Markdown evaluation report."""
    console.print(f"[bold green]EvalGate Report Generator[/bold green]")
    console.print(f"Run dir: {run_dir}")
    console.print(f"Format: {format}")
    console.print("[yellow]⚠ Report generator not yet implemented (M7).[/yellow]")


@app.command()
def version() -> None:
    """Print the EvalGate version."""
    console.print(f"evalgate {__version__}")


if __name__ == "__main__":
    app()
