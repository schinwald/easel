import sys
import typer

from .loader import load_config
from .processor import process_line


def command(config: str = typer.Option(help="Path to TOML config file")):
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

