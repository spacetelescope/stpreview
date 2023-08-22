from pathlib import Path

from roman_datamodels.maker_utils import (
    mk_level1_science_raw,
    mk_level2_image,
    mk_level3_mosaic,
)

OUTPUT_DIRECTORY = Path(__file__).parent.parent / "data"


if __name__ == "__main__":
    mk_level1_science_raw(filepath=OUTPUT_DIRECTORY / "level1_science_raw.asdf")
    mk_level2_image(filepath=OUTPUT_DIRECTORY / "level2_image.asdf")
    mk_level3_mosaic(filepath=OUTPUT_DIRECTORY / "level3_mosaic.asdf")
