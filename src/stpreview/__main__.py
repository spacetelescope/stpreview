from pathlib import Path

import typer

from stpreview.downsample import downsample_asdf

app = typer.Typer()


@app.command()
def to(resolution: tuple[int, int], input: Path, output: Path):
    print(f"{resolution} {input} -> {output}")


@app.command()
def by(factor: float, input: Path, output: Path):
    downsample_asdf(input=input, by=factor, output=output)


def command():
    app()


if __name__ == "__main__":
    command()
