from pathlib import Path

import asdf
from matplotlib import pyplot
from roman_datamodels.maker_utils import (
    mk_level1_science_raw,
    mk_level2_image,
    mk_level3_mosaic,
)

OUTPUT_DIRECTORY = Path(__file__).parent.parent / "data"


if __name__ == "__main__":
    level1 = OUTPUT_DIRECTORY / "level1_science_raw.asdf"
    level2 = OUTPUT_DIRECTORY / "level2_image.asdf"
    level3 = OUTPUT_DIRECTORY / "level3_mosaic.asdf"

    if not level1.exists():
        mk_level1_science_raw(filepath=level1)

    if not level2.exists():
        mk_level2_image(filepath=level2)

    if not level3.exists():
        mk_level3_mosaic(filepath=level3)

    with asdf.open(level1) as file:
        print(file.info())
        print(file["roman"]["data"].shape)

    with asdf.open(level2) as file:
        print(file.info())
        pyplot.imshow(file["roman"]["data"])

    pyplot.show()

    # with asdf.open(level3) as file:
    #     pyplot.imshow(file['roman']['data'])

    # pyplot.show()
