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

    ds1 = drop_rows(ds, skip_perc=20, power2=False)
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


def test_power2():
    """Test dropping with power-of-2."""

    ds = parse_ds("tests/data/dr-01-long.dat", None, True)
    assert ds.shape == (119, 4)

    ds1 = drop_rows(ds, skip_perc=20, power2=True)
    assert ds1.shape == (64, 4)
    assert np.array_equal(
        ds1[0],
        np.array(
            [0.83069127, 0.52074408, 0.07777817, 0.95200611]
        ),
    )
    assert np.array_equal(
        ds1[13],
        np.array(
            [0.17146188, 0.08339644, 0.579845, 0.81871138]
        ),
    )
    assert np.array_equal(
        ds1[-1],
        np.array(
            [0.61788947, 0.63002014, 0.93538286, 0.45439481]
        ),
    )

    ds2 = drop_rows(ds, skip_perc=60, power2=True)
    assert ds2.shape == (32, 4)
    assert np.array_equal(
        ds2[0],
        np.array(
            [0.69626567, 0.73732882, 0.58448449, 0.58103998]
        ),
    )
    assert np.array_equal(
        ds2[5],
        np.array(
            [0.6665143, 0.90572339, 0.92537975, 0.2026005]
        ),
    )
    assert np.array_equal(
        ds2[-1],
        np.array(
            [0.61788947, 0.63002014, 0.93538286, 0.45439481]
        ),
    )


def test_single():
    """Test single-column file, filtered and natural, w/ and w/o power of 2."""

    ds = parse_ds(
        "tests/data/dr-01-long.dat",
        fields=[2],
        colnum_test=True,
    )

    # filtered, w/o power of 2
    ds1 = drop_rows(ds, skip_perc=20, power2=False)
    assert ds1.shape == (96, 1)
    assert ds1[0] == [0.94791775]
    assert ds1[52] == [0.6738459]
    assert ds1[-1] == [0.93538286]

    # filtered, w/ power of 2
    ds2 = drop_rows(ds, skip_perc=20, power2=True)
    assert ds2.shape == (64, 1)
    assert ds2[0] == [0.07777817]
    assert ds2[13] == [0.579845]
    assert ds2[-1] == [0.93538286]

    ds = parse_ds(
        "tests/data/dr-02-single_column.dat",
        fields=None,
        colnum_test=True,
    )

    # natural, w/o power of 2
    ds1 = drop_rows(ds, skip_perc=20, power2=False)
    assert ds1.shape == (96, 1)
    assert ds1[0] == [0.94791775]
    assert ds1[52] == [0.6738459]
    assert ds1[-1] == [0.93538286]

    # filtered, w/ power of 2
    ds2 = drop_rows(ds, skip_perc=20, power2=True)
    assert ds2.shape == (64, 1)
    assert ds2[0] == [0.07777817]
    assert ds2[13] == [0.579845]
    assert ds2[-1] == [0.93538286]


def test_short():
    """Test file where too many rows are skipped."""

    ds = parse_ds(
        "tests/data/dr-03-short.dat", None, colnum_test=True
    )

    with pytest.raises(TailoringError) as err:
        ds1 = drop_rows(ds, skip_perc=90, power2=True)
        assert ds1.shape == (1, 1)
    assert str(err.value) == "insufficient number of rows"
