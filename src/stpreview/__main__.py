from pathlib import Path
from typing import Union

import numpy
import typer
from astropy.visualization import (
    BaseStretch,
    ImageNormalize,
    LinearStretch,
    PercentileInterval,
)
from matplotlib import pyplot
from matplotlib.colors import Colormap

from stpreview.downsample import downsample_asdf_by, downsample_asdf_to

app = typer.Typer()


def percentile_normalization(
    data: numpy.ndarray, percentile: float, stretch: BaseStretch = None
) -> ImageNormalize:
    """
    stretch the given data based on the given percentile
    """

    if stretch is None:
        stretch = LinearStretch()

    interval = PercentileInterval(percentile)
    vmin, vmax = interval.get_limits(data)

    normalization = ImageNormalize(vmin=vmin, vmax=vmax, stretch=stretch)

    return normalization


def write_image(
    data: numpy.ndarray,
    output: Path,
    normalization: ImageNormalize = None,
    colormap: Union[str, Colormap] = None,
):
    """
    write data as an image to the given path
    """

    if normalization is None:
        normalization = percentile_normalization(data, percentile=90)

    if colormap is None:
        colormap = "afmhot"

    figure = pyplot.figure()
    axis = figure.add_subplot(1, 1, 1)
    axis.imshow(data, norm=normalization, cmap=colormap)
    axis.savefig(output, bbox_inches="tight")


@app.command()
def downsample_by(input: Path, factor: tuple[int, int], output: Path):
    data = downsample_asdf_by(input=input, by=factor)

    write_image(data, output)


@app.command()
def downsample_to(
    input: Path, resolution: tuple[int, int], output: Path, observatory: str = None
):
    data = downsample_asdf_to(resolution, input, observatory)

    write_image(data, output)


def command():
    app()


if __name__ == "__main__":
    command()
