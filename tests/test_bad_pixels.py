import asdf
import numpy
import pytest

from stpreview.downsample import (
    DO_NOT_USE,
    clip_to_percentiles,
    downsample_asdf_by,
)

OBSERVATORY = "roman"
SHAPE = (100, 100)
FACTOR = 20
BAD_VALUE = 1e6


def write_asdf(path, **arrays):
    asdf.AsdfFile({OBSERVATORY: arrays}).write_to(path)
    return path


@pytest.fixture
def data():
    return numpy.random.default_rng(0).normal(1, 0.1, SHAPE).astype(numpy.float32)


def test_clip_to_percentiles(data):
    data[10, 10] = BAD_VALUE
    data[50, 50] = -BAD_VALUE
    data[70, 70] = numpy.nan

    clipped = clip_to_percentiles(data)

    lower, upper = numpy.nanpercentile(data, [1, 99])
    assert clipped[10, 10] == pytest.approx(upper)
    assert clipped[50, 50] == pytest.approx(lower)
    assert numpy.isnan(clipped[70, 70])
    assert numpy.nanmin(clipped) >= lower
    assert numpy.nanmax(clipped) <= upper


def test_clip_to_percentiles_all_nan():
    data = numpy.full(SHAPE, numpy.nan)
    assert numpy.all(numpy.isnan(clip_to_percentiles(data)))


def test_do_not_use_masked(data, tmp_path):
    # flag an entire block, plus single pixels with other flags set
    dq = numpy.zeros(SHAPE, dtype=numpy.uint32)
    dq[:FACTOR, :FACTOR] = DO_NOT_USE
    dq[30, 30] = DO_NOT_USE | 0b100
    dq[50, 50] = 0b100
    data[30, 30] = BAD_VALUE

    input = write_asdf(tmp_path / "dq.asdf", data=data, dq=dq)
    result = downsample_asdf_by(input, factor=FACTOR, observatory=OBSERVATORY)

    assert result.shape == (5, 5)
    assert numpy.isnan(result[0, 0])
    assert numpy.count_nonzero(numpy.isnan(result)) == 1
    assert numpy.nanmax(numpy.abs(result - 1)) < 0.05


def test_isolated_outliers_without_dq(data, tmp_path):
    # L3 files have no DQ array; outliers should still be suppressed
    data[10, 10] = BAD_VALUE
    data[50, 50] = -BAD_VALUE

    input = write_asdf(tmp_path / "nodq.asdf", data=data)
    result = downsample_asdf_by(input, factor=FACTOR, observatory=OBSERVATORY)

    assert numpy.all(numpy.isfinite(result))
    assert numpy.max(numpy.abs(result - 1)) < 0.05
