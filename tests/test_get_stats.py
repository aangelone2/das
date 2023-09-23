"""Test module for get_stats() function."""


from modules.common import parse_ds
from modules.common import drop_rows
from modules.common import rebin
from modules.common import get_stats


def test_get_stats():
    """Test a sample datafile."""

    ds = parse_ds("tests/data/rb-01-short.dat", None, True)
    ds = drop_rows(ds, skip_perc=30, power2=True)
    ds = rebin(ds, nbins=4)
    assert ds.shape == (4, 3)

    res = get_stats(ds)
    assert res == [
        {
            "m": 3.375,
            "s": 0.5153882032022076,
            "ds": 0.2104063528825433,
            "sum": 13.5,
        },
        {
            "m": 5.125,
            "s": 1.637770333919462,
            "ds": 0.6686169389950505,
            "sum": 20.5,
        },
        {
            "m": 4.0,
            "s": 1.5,
            "ds": 0.6123724356957946,
            "sum": 16.0,
        },
    ]


def test_single_col():
    """Test a single-column dataset."""

    ds = parse_ds("tests/data/rb-01-short.dat", [1], True)
    ds = drop_rows(ds, skip_perc=30, power2=True)
    ds = rebin(ds, nbins=4)
    assert ds.shape == (4, 1)

    res = get_stats(ds)
    assert res == [
        {
            "m": 5.125,
            "s": 1.637770333919462,
            "ds": 0.6686169389950505,
            "sum": 20.5,
        }
    ]