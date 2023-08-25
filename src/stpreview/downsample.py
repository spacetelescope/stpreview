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
            return None


def downsample_asdf(
    input: Path, by: int, func=numpy.max, observatory: str = None
) -> numpy.ndarray:
    if observatory is None:
        observatory = asdf_observatory(input)

    with asdf.open(input) as file:
        return block_reduce(file[observatory]["data"], func=func)
