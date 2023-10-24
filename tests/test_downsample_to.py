import asdf
import numpy
import pytest
from PIL import Image
from test_data import (
    DATA_DIRECTORY,
    SHARED_DATA_DIRECTORY,
    level1_science_raw,
    level2_image,
    level3_mosaic,
)
from typer.testing import CliRunner

from stpreview.__main__ import app
from stpreview.downsample import downsample_asdf_to

OBSERVATORY = "roman"


@pytest.mark.parametrize(
    "input",
    [
        level1_science_raw(DATA_DIRECTORY),
        level2_image(DATA_DIRECTORY),
        level3_mosaic(DATA_DIRECTORY),
    ],
)
@pytest.mark.parametrize(
    "shape",
    [(1080, 1080), (300, 300)],
)
def test_dummy_data(input, shape):
    with asdf.open(input) as file:
        original_shape = file[OBSERVATORY]["data"].shape

    if len(original_shape) != len(shape):
        shape = numpy.concatenate(
            [[original_shape[index] for index in range(len(original_shape) - 2)], shape]
        )

    assert numpy.any(original_shape != shape)

    result = downsample_asdf_to(input, to=shape)

    assert numpy.all(numpy.array(result.shape) <= shape)


runner = CliRunner()


@pytest.mark.parametrize(
    "input",
    [
        level2_image(DATA_DIRECTORY),
        level3_mosaic(DATA_DIRECTORY),
    ],
)
@pytest.mark.parametrize(
    "shape",
    [2, 4],
)
def test_command(input, shape, tmp_path):
    with asdf.open(input) as file:
        original_shape = file[OBSERVATORY]["data"].shape

    if len(original_shape) != len(shape):
        shape = numpy.concatenate(
            [[original_shape[index] for index in range(len(original_shape) - 2)], shape]
        )

    assert numpy.any(original_shape != shape)

    result = downsample_asdf_to(input, to=shape)

    output = tmp_path / f"{input.stem}.png"

    status = runner.invoke(app, ["downsample", "to", input, output, *shape])
    assert status.exit_code == 0

    image = Image.open(output)
    result = numpy.asarray(image)

    assert numpy.all(numpy.array(result.shape) <= shape)


@pytest.mark.shareddata
@pytest.mark.skipif(
    not SHARED_DATA_DIRECTORY.exists(), reason="can't reach shared data directory"
)
@pytest.mark.parametrize(
    "input",
    [
        filename
        for filename in SHARED_DATA_DIRECTORY.iterdir()
        if filename.suffix.lower() == ".asdf"
    ]
    if SHARED_DATA_DIRECTORY.exists()
    else [],
)
@pytest.mark.parametrize(
    "shape",
    [(1080, 1080), (300, 300)],
)
def test_sample_data(input, shape):
    with asdf.open(input) as file:
        original_shape = file[OBSERVATORY]["data"].shape

    if len(original_shape) != len(shape):
        shape = numpy.concatenate(
            [[original_shape[index] for index in range(len(original_shape) - 2)], shape]
        )

    assert numpy.any(original_shape != shape)

    result = downsample_asdf_to(input, to=shape)

    assert numpy.all(numpy.array(result.shape) <= shape)
