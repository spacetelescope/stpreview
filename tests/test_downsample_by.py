from pathlib import Path

import asdf
import pytest

from stpreview.downsample import downsample_asdf_by

OBSERVATORY = "roman"

DATA_DIRECTORY = Path(__file__).parent / "data"
if not DATA_DIRECTORY.exists():
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

SHARED_DATA_DIRECTORY = Path("/grp/roman/TEST_DATA/23Q4_B11/aligntest")


def level1_science_raw(data_directory) -> Path:
    filename = data_directory / "level1_science_raw.asdf"
    if not filename.exists():
        from roman_datamodels.maker_utils import mk_level1_science_raw

        mk_level1_science_raw(filepath=filename)

    return filename


def level2_image(data_directory) -> Path:
    filename = data_directory / "level2_image.asdf"
    if not filename.exists():
        from roman_datamodels.maker_utils import mk_level2_image

        mk_level2_image(filepath=filename)

    return filename


def level3_mosaic(data_directory) -> Path:
    filename = data_directory / "level3_mosaic.asdf"
    if not filename.exists():
        from roman_datamodels.maker_utils import mk_level3_mosaic

        mk_level3_mosaic(filepath=filename)

    return filename


@pytest.mark.parametrize(
    "filename",
    [
        level1_science_raw(DATA_DIRECTORY),
        level2_image(DATA_DIRECTORY),
        level3_mosaic(DATA_DIRECTORY),
    ],
)
@pytest.mark.parametrize(
    "by",
    [2, 4],
)
def test_dummy_data(filename, by):
    with asdf.open(filename) as file:
        shape = file[OBSERVATORY]["data"].shape

    downsampled_shape = tuple(
        dimension if index < len(shape) - 2 else int(dimension / by)
        for index, dimension in enumerate(shape)
    )
    assert shape != downsampled_shape

    result = downsample_asdf_by(filename, by=by)

    assert result.shape == downsampled_shape


@pytest.mark.shareddata
@pytest.mark.skipif(
    not SHARED_DATA_DIRECTORY.exists(), reason="can't reach shared data directory"
)
@pytest.mark.parametrize(
    "filename",
    [
        filename
        for filename in SHARED_DATA_DIRECTORY.iterdir()
        if filename.suffix.lower() == ".asdf"
    ]
    if SHARED_DATA_DIRECTORY.exists()
    else [],
)
@pytest.mark.parametrize(
    "by",
    [2, 4],
)
def test_sample_data(filename, by):
    with asdf.open(filename) as file:
        shape = file[OBSERVATORY]["data"].shape

    downsampled_shape = tuple(
        dimension if index < len(shape) - 2 else int(dimension / by)
        for index, dimension in enumerate(shape)
    )
    assert shape != downsampled_shape

    result = downsample_asdf_by(filename, by=by)

    assert result.shape == downsampled_shape
