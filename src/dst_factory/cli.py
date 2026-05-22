import typer
from rich.console import Console

from dst_factory.drive.client import GoogleDriveClient

app = typer.Typer(no_args_is_help=True)
console = Console()

drive_app = typer.Typer(no_args_is_help=True)
app.add_typer(drive_app, name="drive")


@app.callback()
def main() -> None:
    """Nyvia DST Factory CLI."""


@app.command()
def doctor() -> None:
    """Validate CLI."""
    console.print("[green]DST Factory OK[/green]")


@drive_app.command("auth")
def drive_auth() -> None:
    """Authenticate against Google Drive."""
    client = GoogleDriveClient()
    client.authenticate()

    console.print("[green]Google Drive authenticated[/green]")


if __name__ == "__main__":
    app()