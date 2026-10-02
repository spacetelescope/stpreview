import numpy
from matplotlib import image

from stpreview.image import write_image


def test_no_border(tmp_path):
    output = tmp_path / "image.png"
    write_image(numpy.zeros((50, 50)), output, shape=(100, 100))

    # the image fills the requested shape, with no white margin
    result = image.imread(output)
    assert result.shape[:2] == (100, 100)
    assert not numpy.any(numpy.all(result[..., :3] == 1, axis=-1))
