"""CLI entry point."""

import typer
from whendoes.cli.repl import run_repl
from whendoes.cli.setup import setup_wizard, show_provider_info

app = typer.Typer(help="Whendoes CLI - Control Windows via natural language")


@app.command()
def main() -> None:
    """Start interactive CLI."""
    run_repl()


@app.command()
def setup() -> None:
    """Configure LLM provider and API keys."""
    setup_wizard()


@app.command()
def info() -> None:
    """Show information about available LLM providers."""
    show_provider_info()


if __name__ == "__main__":
    app()
