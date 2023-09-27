"""Test module for rebin() function."""


import numpy as np
import pytest

from modules.common import TailoringError
from modules.common import parse_ds
from modules.common import drop_rows
from modules.common import rebin


def test_successful():
    """Test a successful binning schema."""

    ds = parse_ds("tests/data/rb-01-short.dat", None, True)
    ds = drop_rows(ds, skip_perc=30, nbins=8)
    assert ds.shape == (8, 3)

    ds1 = rebin(ds, nbins=4)
    assert np.array_equal(
        ds1,
        np.array(
            [
                [4, 1, 0.5],
                [2.5, 5.5, 6.5],
                [2.5, 9, 2.5],
                [4.5, 5, 6.5],
            ]
        ),
    )

    ds2 = rebin(ds, nbins=2)
    assert np.array_equal(
        ds2, np.array([[3.25, 3.25, 3.5], [3.5, 7, 4.5]])
    )


def test_failure():
    """Test failures in binning schemas."""

    ds = parse_ds("tests/data/rb-01-short.dat", None, True)
    ds = drop_rows(ds, skip_perc=30, nbins=8)
    assert ds.shape == (8, 3)

    with pytest.raises(TailoringError) as err:
        _ = rebin(ds, nbins=10)
    assert str(err.value) == "insufficient rows for binning"

    with pytest.raises(TailoringError) as err:
        _ = rebin(ds, nbins=5)
    assert str(err.value) == "leftover rows in binning"


def test_single():
    """Test binning with single column."""

    ds = parse_ds("tests/data/rb-01-short.dat", [1], True)
    ds = drop_rows(ds, skip_perc=30, nbins=8)
    assert ds.shape == (8, 1)

    ds1 = rebin(ds, nbins=4)
    assert np.array_equal(
        ds1,
        np.array(
            [
                [
                    1,
                ],
                [
                    5.5,
                ],
                [
                    9,
                ],
                [
                    5,
                ],
            ]
        ),
    )

    ds2 = rebin(ds, nbins=2)
    assert np.array_equal(
        ds2,
        np.array(
            [
                [
                    3.25,
                ],
                [
                    7,
                ],
            ]
        ),
    )
