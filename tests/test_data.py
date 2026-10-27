from pathlib import Path

SHARED_DATA_DIRECTORY = Path("/grp/roman/TEST_DATA/23Q4_B11/aligntest")

DATA_DIRECTORY = Path(__file__).parent / "data"
if not DATA_DIRECTORY.exists():
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)


def level1_science_raw(data_directory) -> Path:
    filename = data_directory / "level1_science_raw.asdf"
    if not filename.exists():
        from roman_datamodels.datamodels import ScienceRawModel

        ScienceRawModel.create_fake_data(shape=(8, 4096, 4096)).save(filename)

    return filename


def level2_image(data_directory) -> Path:
    filename = data_directory / "level2_image.asdf"
    if not filename.exists():
        from roman_datamodels.datamodels import ImageModel

        ImageModel.create_fake_data(shape=(4088, 4088)).save(filename)

    return filename


def level3_mosaic(data_directory) -> Path:
    filename = data_directory / "level3_mosaic.asdf"
    if not filename.exists():
        from roman_datamodels.datamodels import MosaicModel

        MosaicModel.create_fake_data(shape=(5000, 5000)).save(filename)

    return filename
