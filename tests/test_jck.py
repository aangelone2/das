"""Test module for jck() driver."""


from modules.functionals import susceptibility

from modules.common import parse_ds
from modules.drivers import jck


def test_simple():
    """Test a simple averaging scheme."""

    SKIP_PERC = 10

    ds = parse_ds("tests/data/jck-01.dat.gz", [2, 3], True)
    stats, report = jck(ds, SKIP_PERC, susceptibility)

    assert report == "4096/5000 rows"

    assert stats.nbins == [1024, 512, 256, 128, 64]
    assert stats.bsize == [4, 8, 16, 32, 64]
    assert stats.m == [
        0.24953416366359266,
        0.2495346346160966,
        0.2495332597185667,
        0.24953439999595842,
        0.24954038828181327,
    ]
    assert stats.s == [
        0.006334335765791322,
        0.006268252411588054,
        0.006176007721669315,
        0.005720702847043817,
        0.006487288533114708,
    ]
    assert stats.ds == [
        0.00014003876295128526,
        0.0001960744604143795,
        0.0002734782185760458,
        0.00035894882108480344,
        0.0005779335966681555,
    ]
