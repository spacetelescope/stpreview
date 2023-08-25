from pathlib import Path

import asdf


def downsample_asdf(input: Path, by: int, output: Path):
    with asdf.open(input) as file:
        print(file.info())
