"""Test module for avs() driver."""


from modules.common import parse_ds
from modules.drivers import avs


def test_simple():
    """Test a simple averaging scheme."""

    SKIP_PERC = 20

    ds = parse_ds("tests/data/avs-01.dat.gz", None, True)
    stats, report = avs(ds, SKIP_PERC)

    assert report == "8000/10000 rows"

    assert stats.m == [
        0.502596645631248,
        0.498392322922783,
        0.5029735829100479,
    ]
    assert stats.s == [
        0.0032166135733013423,
        0.003192300587095481,
        0.0032306606710632837,
    ]
    assert stats.ds == [
        2.543115260732433e-05,
        2.523892956018148e-05,
        2.5542211607335726e-05,
    ]


def test_single_column():
    """Test a single-column averaging scheme."""

    SKIP_PERC = 20

    # simple
    ds = parse_ds("tests/data/avs-01.dat.gz", [2], True)
    stats, report = avs(ds, SKIP_PERC)

    assert report == "8000/10000 rows"

    assert stats.m == [0.5029735829100479]
    assert stats.s == [0.0032306606710632837]
    assert stats.ds == [2.5542211607335726e-05]
