import sys
from typing import Annotated
import typer

from src.loader import load_config
from src.processor import process_line

app = typer.Typer()


def get_version(version: bool | None):
    if version:
        typer.echo("0.2.0")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    config: Annotated[
        str,
        typer.Option(
            "--config", "-c", help="path to toml config file", show_envvar=False
        ),
    ],
    _version: Annotated[
        bool | None,
        typer.Option(
            "--version", help="display the version of easel", callback=get_version
        ),
    ] = None,
):
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
