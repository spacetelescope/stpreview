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
from stpreview.downsample import downsample_asdf_by

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
    "factor",
    [2, 4],
)
def test_dummy_data(input, factor):
    with asdf.open(input) as file:
        original_shape = file[OBSERVATORY]["data"].shape

    downsampled_shape = tuple(
        dimension if index < len(original_shape) - 2 else int(dimension / factor)
        for index, dimension in enumerate(original_shape)
    )
    assert original_shape != downsampled_shape

    result = downsample_asdf_by(input, factor=factor)

    assert result.shape == downsampled_shape


runner = CliRunner()


@pytest.mark.parametrize(
    "input",
    [
        level2_image(DATA_DIRECTORY),
        level3_mosaic(DATA_DIRECTORY),
    ],
)
@pytest.mark.parametrize(
    "factor",
    [2, 4],
)
def test_command(input, factor, tmp_path):
    with asdf.open(input) as file:
        original_shape = file[OBSERVATORY]["data"].shape

    downsampled_shape = tuple(
        dimension if index < len(original_shape) - 2 else int(dimension / factor)
        for index, dimension in enumerate(original_shape)
    )
    assert original_shape != downsampled_shape

    output = tmp_path / f"{input.stem}.png"

    result = runner.invoke(app, ["downsample", "by", input, output, *factor])
    assert result.exit_code == 0

    image = Image.open(output)
    data = numpy.asarray(image)

    assert data.shape == downsampled_shape


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
    "factor",
    [2, 4],
)
def test_sample_data(input, factor):
    with asdf.open(input) as file:
        original_shape = file[OBSERVATORY]["data"].shape

    downsampled_shape = tuple(
        dimension if index < len(original_shape) - 2 else int(dimension / factor)
        for index, dimension in enumerate(original_shape)
    )
    assert original_shape != downsampled_shape

    result = downsample_asdf_by(input, factor=factor)

    assert result.shape == downsampled_shape
