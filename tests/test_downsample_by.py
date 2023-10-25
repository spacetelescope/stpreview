import asdf
import pytest
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

    downsampled_shape = [1 for _ in original_shape]
    downsampled_shape[-2] = int(original_shape[-2] / factor)
    downsampled_shape[-1] = int(original_shape[-1] / factor)
    downsampled_shape = tuple(downsampled_shape)
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
    [2, 4, (2, 4)],
)
def test_command(input, factor, tmp_path):
    with asdf.open(input) as file:
        original_shape = file[OBSERVATORY]["data"].shape

    downsampled_shape = tuple(
        dimension if index < len(original_shape) - 2 else int(dimension / factor)
        for index, dimension in enumerate(original_shape)
    )
    downsampled_shape = [1 for _ in original_shape]
    downsampled_shape[-2] = int(original_shape[-2] / factor)
    downsampled_shape[-1] = int(original_shape[-1] / factor)
    downsampled_shape = tuple(downsampled_shape)
    assert original_shape != downsampled_shape

    output = tmp_path / f"{input.stem}.png"

    status = runner.invoke(app, [str(value) for value in ("by", input, output, factor)])
    assert status.exit_code == 0


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

    downsampled_shape = [1 for _ in original_shape]
    downsampled_shape[-2] = int(original_shape[-2] / factor)
    downsampled_shape[-1] = int(original_shape[-1] / factor)
    downsampled_shape = tuple(downsampled_shape)
    assert original_shape != downsampled_shape

    result = downsample_asdf_by(input, factor=factor)

    assert result.shape == downsampled_shape
