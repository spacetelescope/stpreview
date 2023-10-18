from pathlib import Path

import asdf
import typer

from stpreview.downsample import downsample_asdf_by, downsample_asdf_to

app = typer.Typer()


@app.command()
def downsample_to(
    resolution: tuple[int, int], input: Path, output: Path, observatory: str = None
):
    data = downsample_asdf_to(resolution, input, observatory)

    with asdf.open(output, mode="rw") as file:
        file.write(data)


@app.command()
def downsample_by(factor: tuple[int, int], input: Path, output: Path):
    data = downsample_asdf_by(input=input, by=factor)

    with asdf.open(output, mode="rw") as file:
        file.write(data)


def command():
    app()


if __name__ == "__main__":
    command()
