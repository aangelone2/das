"""Test module for drop_rows() function."""


import numpy as np
import pytest

from modules.common import TailoringError
from modules.common import parse_ds
from modules.common import drop_rows


def test_simple():
    """Test dropping without power-of-2."""

    ds = parse_ds("tests/data/dr-01-long.dat", None, True)
    assert ds.shape == (119, 4)

    ds1 = drop_rows(ds, skip_perc=20, nbins=None)
    assert ds1.shape == (96, 4)
    assert np.array_equal(
        ds1[0],
        np.array(
            [0.79257095, 0.79830817, 0.94791775, 0.06518289]
        ),
    )
    assert np.array_equal(
        ds1[52],
        np.array(
            [0.51715544, 0.96024379, 0.6738459, 0.80586979]
        ),
    )
    assert np.array_equal(
        ds1[-1],
        np.array(
            [0.61788947, 0.63002014, 0.93538286, 0.45439481]
        ),
    )


def test_nbins():
    """Test dropping with selected number of bins."""

    ds = parse_ds("tests/data/dr-01-long.dat", None, True)
    assert ds.shape == (119, 4)

    ds1 = drop_rows(ds, skip_perc=20, nbins=15)
    assert ds1.shape == (90, 4)
    assert np.array_equal(
        ds1[0],
        np.array(
            [0.27288035, 0.62491234, 0.50501386, 0.35869342]
        ),
    )
    assert np.array_equal(
        ds1[13],
        np.array(
            [0.59794363, 0.58962945, 0.65848451, 0.43271424]
        ),
    )
    assert np.array_equal(
        ds1[-1],
        np.array(
            [0.61788947, 0.63002014, 0.93538286, 0.45439481]
        ),
    )

    ds2 = drop_rows(ds, skip_perc=60, nbins=15)
    assert ds2.shape == (45, 4)
    assert np.array_equal(
        ds2[0],
        np.array(
            [0.71912613, 0.3420949, 0.99502956, 0.50921441]
        ),
    )
    assert np.array_equal(
        ds2[5],
        np.array(
            [0.32173851, 0.59395812, 0.03953717, 0.68371832]
        ),
    )
    assert np.array_equal(
        ds2[-1],
        np.array(
            [0.61788947, 0.63002014, 0.93538286, 0.45439481]
        ),
    )


def test_single():
    """Test single-column file, filtered and natural, w/ and w/o nbins."""

    ds = parse_ds(
        "tests/data/dr-01-long.dat",
        fields=[2],
        colnum_test=True,
    )

    # filtered, w/o nbins
    ds1 = drop_rows(ds, skip_perc=20, nbins=None)
    assert ds1.shape == (96, 1)
    assert ds1[0] == [0.94791775]
    assert ds1[52] == [0.6738459]
    assert ds1[-1] == [0.93538286]

    # filtered, w/ nbins
    ds2 = drop_rows(ds, skip_perc=20, nbins=15)
    assert ds2.shape == (90, 1)
    assert ds2[0] == [0.50501386]
    assert ds2[13] == [0.65848451]
    assert ds2[-1] == [0.93538286]

    ds = parse_ds(
        "tests/data/dr-02-single_column.dat",
        fields=None,
        colnum_test=True,
    )

    # natural, w/o nbins
    ds1 = drop_rows(ds, skip_perc=20, nbins=None)
    assert ds1.shape == (96, 1)
    assert ds1[0] == [0.94791775]
    assert ds1[52] == [0.6738459]
    assert ds1[-1] == [0.93538286]

    # filtered, w/ nbins
    ds2 = drop_rows(ds, skip_perc=20, nbins=15)
    assert ds2.shape == (90, 1)
    assert ds2[0] == [0.50501386]
    assert ds2[13] == [0.65848451]
    assert ds2[-1] == [0.93538286]


def test_short():
    """Test file where too many rows are skipped."""

    ds = parse_ds(
        "tests/data/dr-03-short.dat", None, colnum_test=True
    )

    with pytest.raises(TailoringError) as err:
        ds1 = drop_rows(ds, skip_perc=90, nbins=8)
        assert ds1.shape == (1, 1)
    assert str(err.value) == "insufficient rows left"
