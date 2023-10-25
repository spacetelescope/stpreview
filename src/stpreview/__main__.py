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
    shape: tuple[int, int] = None,
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

    if shape is None:
        shape = data.shape

    dpi = 100
    figure = pyplot.figure(figsize=numpy.array(shape) / dpi)
    axis = figure.add_subplot(1, 1, 1)
    axis.imshow(data, norm=normalization, cmap=colormap)
    pyplot.axis("off")
    figure.savefig(output, dpi=dpi, bbox_inches="tight")


@app.command()
def by(input: Path, output: Path, factor: list[int]):
    parsed_factor = factor[0] if len(factor) == 1 else tuple(factor)

    data = downsample_asdf_by(input=input, factor=parsed_factor)

    write_image(data, output)


@app.command()
def to(
    input: Path,
    output: Path,
    shape: list[int],
    observatory: str = None,
):
    parsed_shape: Union[int, tuple[int, ...]] = (
        shape[0] if len(shape) == 1 else tuple(shape)
    )

    data = downsample_asdf_to(input=input, shape=parsed_shape, observatory=observatory)

    write_image(data, output, shape=parsed_shape)


def main():
    app()


if __name__ == "__main__":
    main()
