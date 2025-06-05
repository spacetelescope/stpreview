# Space Telescope Product Downsampling

[![Powered by STScI Badge](https://img.shields.io/badge/powered%20by-STScI-blue.svg?colorA=707170&colorB=3e8ddd&style=flat)](http://www.stsci.edu)
[![Powered by Astropy Badge](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)
[![build](https://github.com/spacetelescope/stpreview/actions/workflows/build.yml/badge.svg)](https://github.com/spacetelescope/stpreview/actions/workflows/build.yml)
[![test](https://github.com/spacetelescope/stpreview/actions/workflows/tests.yml/badge.svg)](https://github.com/spacetelescope/stpreview/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/spacetelescope/stpreview/graph/badge.svg?token=tSEFJ5vwgH)](https://codecov.io/gh/spacetelescope/stpreview)

```
pip install stpreview
```

### Usage

```
❯ uv run stpreview --help
usage: stpreview [-h] [--observatory {roman,jwst}] [--compass]
                 INPUT OUTPUT {to,by} ...

positional arguments:
  INPUT                 path to ASDF file with 2D image data
  OUTPUT                path to output image file
  {to,by}
    to                  downsample the given ASDF image by the given integer
                        factor
    by                  downsample the given ASDF image to the desired shape (the
                        output image may be smaller than the desired shape, if no
                        even factor exists)

options:
  -h, --help            show this help message and exit
  --observatory {roman,jwst}
                        (if omitted, will attempt to infer from file)
  --compass             draw a north arrow on the image
```

#### `stpreview by`

```
❯ uv run stpreview input.asdf output.png by --help
usage: stpreview INPUT OUTPUT by [-h] factor [factor ...]

positional arguments:
  factor      block size by which to downsample image data

options:
  -h, --help  show this help message and exit
```

#### `stpreview to`

```
❯ uv run stpreview input.asdf output.png to --help
usage: stpreview INPUT OUTPUT to [-h] shape [shape ...]

positional arguments:
  shape       desired pixel resolution of output image

options:
  -h, --help  show this help message and exit
```

### Examples

##### downsample a sample Roman image by a factor of 10, and add a compass rose

```shell
stpreview /grp/roman/TEST_DATA/23Q4_B11/aligntest/r0000501001001001001_01101_0001_WFI01_cal.asdf docs/images/by.png --compass by 10 10
```

![by](./docs/images/by.png)

##### downsample a sample Roman image to within 300x300 pixels

```shell
stpreview /grp/roman/TEST_DATA/23Q4_B11/aligntest/r0000501001001001001_01101_0001_WFI01_cal.asdf docs/images/to.png to 300 300
```

![to](./docs/images/to.png)
