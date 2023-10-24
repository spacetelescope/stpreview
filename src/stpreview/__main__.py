from pathlib import Path

import typer
from PIL import Image

from stpreview.downsample import downsample_asdf_by, downsample_asdf_to

app = typer.Typer()


@app.command()
def downsample_by(factor: tuple[int, int], input: Path, output: Path):
    data = downsample_asdf_by(input=input, by=factor)

    image = Image.fromarray(data)
    image.save(output)


@app.command()
def downsample_to(
    resolution: tuple[int, int], input: Path, output: Path, observatory: str = None
):
    data = downsample_asdf_to(resolution, input, observatory)

    image = Image.fromarray(data)
    image.save(output)


def command():
    app()


if __name__ == "__main__":
    command()
