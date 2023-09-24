"""Test module for avs() driver."""


from modules.common import MAXBINS
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


def test_power2():
    """Test a power2 averaging scheme."""

    SKIP_PERC = 20
    POWER2 = True

    ds = parse_ds("tests/data/avs-01.dat.gz", None, True)
    stats, report = avs(ds, SKIP_PERC, POWER2)

    assert report == f"4096/10000 rows :: {MAXBINS} bins"

    assert stats[0] == {
        "m": 0.5087484968393992,
        "s": 0.004475783615685836,
        "ds": 9.895010683886187e-05,
    }
    assert stats[1] == {
        "m": 0.49746176654938834,
        "s": 0.004499257924593984,
        "ds": 9.946907414690806e-05,
    }
    assert stats[2] == {
        "m": 0.49810783234743905,
        "s": 0.004635024402134489,
        "ds": 0.00010247058373970599,
    }


def test_single_column():
    """Test a single-column averaging scheme."""

    SKIP_PERC = 20

    # simple
    ds = parse_ds("tests/data/avs-01.dat.gz", [2], True)
    stats, report = avs(ds, SKIP_PERC, power2=False)

    assert report == "8000/10000 rows :: 8000 bins"
    assert stats[0] == {
        "m": 0.5029735829100479,
        "s": 0.0032306606710632837,
        "ds": 2.5542211607335726e-05,
    }

    # power-2
    ds = parse_ds("tests/data/avs-01.dat.gz", [0], True)
    stats, report = avs(ds, SKIP_PERC, power2=True)

    assert report == f"4096/10000 rows :: {MAXBINS} bins"
    assert stats[0] == {
        "m": 0.5087484968393992,
        "s": 0.004475783615685836,
        "ds": 9.895010683886187e-05,
    }
