from pathlib import Path

import asdf
import pytest


@pytest.fixture
def data_directory() -> Path:
    return Path(__file__).parent / "data"


@pytest.fixture
def level1_science_raw(data_directory) -> Path:
    filename = data_directory / "level1_science_raw.asdf"
    if not filename.exists():
        from roman_datamodels.maker_utils import mk_level1_science_raw

        mk_level1_science_raw(filepath=filename)


@pytest.fixture
def level2_image(data_directory) -> Path:
    filename = data_directory / "level2_image.asdf"
    if not filename.exists():
        from roman_datamodels.maker_utils import mk_level2_image

        mk_level2_image(filepath=filename)


@pytest.fixture
def level3_mosaic(data_directory) -> Path:
    filename = data_directory / "level3_mosaic.asdf"
    if not filename.exists():
        from roman_datamodels.maker_utils import mk_level3_mosaic

        mk_level3_mosaic(filepath=filename)


def test_level1(level1_science_raw):
    with asdf.open(level1_science_raw) as file:
        print(file.info())
        file["roman"]["data"]


def test_level2(level2_image):
    with asdf.open(level2_image) as file:
        file["roman"]["data"]


def test_level3(level3_mosaic):
    with asdf.open(level3_mosaic) as file:
        file["roman"]["data"]
