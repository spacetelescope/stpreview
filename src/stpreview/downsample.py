from pathlib import Path

import asdf
import numpy
from skimage.measure import block_reduce

OBSERVATORIES = ["roman", "jwst"]


def asdf_observatory(input: Path) -> str:
    with asdf.open(input) as file:
        for name in OBSERVATORIES:
            if name in file:
                return name
        else:
            raise KeyError(
                f"no known observatory found in file (out of {OBSERVATORIES})"
            )


def downsample_asdf_by(
    input: Path, by: int, func=numpy.max, observatory: str = None
) -> numpy.ndarray:
    if observatory is None:
        observatory = asdf_observatory(input)

    with asdf.open(input) as file:
        data = file[observatory]["data"]

    block_size = tuple(
        1 if index < len(data.shape) - 2 else by for index in range(len(data.shape))
    )

    return block_reduce(data, block_size=block_size, func=func)


def downsample_asdf_to(
    resolution: tuple[int, int], input: Path, observatory: str = None
) -> numpy.ndarray:
    if observatory is None:
        observatory = asdf_observatory(input)

    with asdf.open(input) as file:
        factor = tuple(
            numpy.ceil(
                numpy.array(file[observatory]["data"].shape) / numpy.array(resolution)
            ).astype(int)
        )

    return downsample_asdf_by(input=input, by=factor)
