import argparse
from pathlib import Path
from typing import Optional

import asdf

from stpreview.downsample import (
    OBSERVATORIES,
    downsample_asdf_by,
    downsample_asdf_to,
    known_asdf_observatory,
)
from stpreview.image import north_pole_angle, write_image


def by(
    input: Path,
    output: Path,
    factor: tuple[int, int],
    observatory: Optional[str] = None,
    compass: Optional[bool] = False,
):
    """
    downsample the given ASDF image by the given factor
    """

    if observatory is None:
        observatory = known_asdf_observatory(input)

    data = downsample_asdf_by(input=input, factor=factor, observatory=observatory)

    if compass:
        with asdf.open(input) as file:
            wcs = file[observatory]["meta"]["wcs"]
        north_arrow_angle = north_pole_angle(wcs).degree - 90
    else:
        north_arrow_angle = None

    write_image(
        data,
        output,
        north_arrow_angle=north_arrow_angle,
    )


def to(
    input: Path,
    output: Path,
    shape: tuple[int, int],
    observatory: Optional[str] = None,
    compass: Optional[bool] = False,
):
    """
    downsample the given ASDF image to the desired shape

    the output image may be smaller than the desired shape, if no even factor exists
    """

    if observatory is None:
        observatory = known_asdf_observatory(input)

    data = downsample_asdf_to(input=input, shape=shape, observatory=observatory)

    if compass:
        with asdf.open(input) as file:
            wcs = file[observatory]["meta"]["wcs"]
        north_arrow_angle = north_pole_angle(wcs).degree - 90
    else:
        north_arrow_angle = None

    write_image(
        data,
        output,
        shape=shape,
        north_arrow_angle=north_arrow_angle,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("INPUT", type=Path, help="path to ASDF file with 2D image data")
    parser.add_argument("OUTPUT", type=Path, help="path to output image file")
    parser.add_argument(
        "--observatory",
        type=str,
        choices=OBSERVATORIES,
        help="(if omitted, will attempt to infer from file)",
        required=False,
    )
    parser.add_argument(
        "--compass",
        action="store_true",
        help="draw a north arrow on the image",
    )

    subparsers = parser.add_subparsers(dest="subcommand")

    to_parser = subparsers.add_parser(
        "to", help="downsample the given ASDF image by the given integer factor"
    )
    to_parser.add_argument(
        "shape",
        type=int,
        nargs="+",
        help="desired pixel shape of output image",
    )
    to_parser.set_defaults(func=to)

    by_parser = subparsers.add_parser(
        "by",
        help="downsample the given ASDF image to the desired shape (the output image may be smaller than the desired shape, if no even factor exists)",
    )
    by_parser.add_argument(
        "factor",
        type=int,
        nargs="+",
        help="integer factor by which to downsample input data",
    )
    by_parser.set_defaults(func=by)

    arguments = parser.parse_args()

    arguments.func(
        arguments.INPUT,
        arguments.OUTPUT,
        arguments.shape if arguments.subcommand == "to" else arguments.factor,
        arguments.observatory,
        arguments.compass,
    )


if __name__ == "__main__":
    main()
