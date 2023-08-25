from pathlib import Path

import asdf
import numpy
import typer

from stpreview.downsample import asdf_observatory, downsample_asdf

app = typer.Typer()


@app.command()
def to(resolution: tuple[int, int], input: Path, output: Path, observatory: str = None):
    if observatory is None:
        observatory = asdf_observatory(input)

    with asdf.open(input) as file:
        factor = tuple(
            numpy.ceil(
                numpy.array(file[observatory]["data"].shape) / numpy.array(resolution)
            ).astype(int)
        )

    data = downsample_asdf(input=input, by=factor)

    with asdf.open(output, mode="rw") as file:
        file.write(data)


@app.command()
def by(factor: tuple[int, int], input: Path, output: Path):
    data = downsample_asdf(input=input, by=factor)

    with asdf.open(output, mode="rw") as file:
        file.write(data)


def command():
    app()


if __name__ == "__main__":
    command()
