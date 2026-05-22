import typer

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """"Nyvia DST Factory CLI."""

@app.command()
def doctor():
    print("DST Factory OK")


if __name__ == "__main__":
    app()