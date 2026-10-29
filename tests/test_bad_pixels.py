import asdf
import numpy

from stpreview.downsample import DO_NOT_USE, downsample_asdf_by

FACTOR = 20


def test_bad_pixels(tmp_path):
    data = numpy.random.default_rng(0).normal(1, 0.1, (100, 100))
    dq = numpy.zeros(data.shape, dtype=numpy.uint32)

    # a fully flagged block is NaN
    dq[:FACTOR, :FACTOR] = DO_NOT_USE

    # an unflagged outlier is clipped; test the low end, since clipping a single
    # high outlier at the 99.999th percentile would need > 10^5 pixels
    data[70, 70] = -1e6

    input = tmp_path / "bad_pixels.asdf"
    asdf.AsdfFile({"roman": {"data": data, "dq": dq}}).write_to(input)
    result = downsample_asdf_by(input, factor=FACTOR)

    assert numpy.isnan(result[0, 0])
    assert numpy.count_nonzero(numpy.isnan(result)) == 1
    # block means have rms ~ 0.1 / 20 = 0.005; allow 10 sigma
    assert numpy.nanmax(numpy.abs(result - 1)) < 0.05
