import sys
import typer

from .loader import load_config
from .processor import process_line


def command(config: str = typer.Option(None, help="Path to TOML config file"), version: bool = typer.Option(False, "--version", help="Show version")):
    if version:
        typer.echo("0.2.0")
        raise typer.Exit()

    if config is None:
        typer.echo("Error: --config is required", err=True)
        raise typer.Exit(1)

    try:
        config_data = load_config(config)
    except ValueError as error:
        typer.echo(error, err=True)
        raise typer.Exit(1)

    # Process input lines
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        processed = process_line(config_data, line.rstrip("\n"))
        typer.echo(processed)
