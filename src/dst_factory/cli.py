import typer
from rich.console import Console

from dst_factory.drive.client import GoogleDriveClient
from dst_factory.sources.extractor import DriveSourceExtractor

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


@drive_app.command("extract")
def drive_extract(folder_id: str) -> None:
    """Extract text from supported files in a Drive folder."""
    extractor = DriveSourceExtractor()
    documents = extractor.extract_folder_document(folder_id)

    for document in documents:
        console.print(f"\n[bold cyan]{document.source_file.name}[/bold cyan]")
        console.print(document.text[:1000])


if __name__ == "__main__":
    app()