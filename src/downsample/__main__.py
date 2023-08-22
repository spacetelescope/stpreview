from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def to(resolution: tuple[int, int], filename: Path):
    print(f"{resolution} {filename}")


@app.command()
def by(factor: float, filename: Path):
    print(f"{factor} {filename}")


def command():
    app()


if __name__ == "__main__":
    command()
