"""Test module for avs() driver."""


from modules.common import parse_ds
from modules.drivers import avs


def test_simple():
    """Test a simple averaging scheme."""

    SKIP_PERC = 20
    POWER2 = False

    ds = parse_ds("tests/data/avs-01.dat.gz", None, True)
    stats, report = avs(ds, SKIP_PERC, POWER2)

    assert report == "8000/10000 rows :: 8000 bins"
    assert stats[0] == {
        "m": 0.502596645631248,
        "s": 0.0032166135733013423,
        "ds": 2.543115260732433e-05,
    }
    assert stats[1] == {
        "m": 0.498392322922783,
        "s": 0.003192300587095481,
        "ds": 2.523892956018148e-05,
    }
    assert stats[2] == {
        "m": 0.5029735829100479,
        "s": 0.0032306606710632837,
        "ds": 2.5542211607335726e-05,
    }
