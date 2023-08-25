from pathlib import Path

import asdf


def downsample_asdf(filename: Path):
    asdf.open(filename)
