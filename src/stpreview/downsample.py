from pathlib import Path
from typing import Union

import asdf
import numpy
from skimage.measure import block_reduce

OBSERVATORIES = ["roman", "jwst"]


def known_asdf_observatory(input: Path, known: list[str] = None) -> str:
    """
    find which observatory key exists in the given ASDF file

    :param input: ASDF file
    :param known: list of known observatory keys
    :returns: first observatory to be found in the file
    """

    if known is None:
        known = OBSERVATORIES

    with asdf.open(input) as file:
        for name in known:
            if name in file:
                return name
        else:
            raise KeyError(
                f"no known observatory found in file (out of {OBSERVATORIES})"
            )


def downsample_asdf_by(
    input: Path,
    by: Union[int, numpy.ndarray],
    func=numpy.max,
    observatory: str = None,
) -> numpy.ndarray:
    """
    downsample an ASDF image by the specified factor

    :param input: ASDF file with 2D image data
    :param by: factor by which to downsample image resolution
    :param func: aggregation function to pass to `skimage.measure.block_reduce`
    :param observatory: space telescope to use
    :returns: downsampled image array
    """

    if observatory is None:
        observatory = known_asdf_observatory(input)

    with asdf.open(input) as file:
        data = file[observatory]["data"].copy()

    if isinstance(by, int):
        block_size = tuple(
            1 if index < len(data.shape) - 2 else by for index in range(len(data.shape))
        )
    else:
        block_size = by

    # for index, dimension in enumerate(data.shape):
    #     if dimension % block_size[index] != 0:
    #         raise RuntimeError(f"{by} is not an even factor of {data.shape}")

    return block_reduce(data, block_size=block_size, func=func)


def downsample_asdf_to(
    input: Path, to: tuple[int, int], func=numpy.max, observatory: str = None
) -> numpy.ndarray:
    """
    attempt to downsample an ASDF image to (near) the specified resolution

    :param input: ASDF file with 2D image data
    :param to: resolution to which to downsample
    :param func: aggregation function to pass to `skimage.measure.block_reduce`
    :param observatory: space telescope to use
    :returns: downsampled image array
    """

    if observatory is None:
        observatory = known_asdf_observatory(input)

    with asdf.open(input) as file:
        factor = tuple(
            numpy.ceil(
                numpy.array(file[observatory]["data"].shape) / numpy.array(to)
            ).astype(int)
        )

    return downsample_asdf_by(input=input, by=factor, func=func)
