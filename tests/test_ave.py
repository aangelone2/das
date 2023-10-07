"""Test module for ave() driver."""


from modules.common import parse_ds
from modules.drivers import ave


def test_ave():
    """Test averaging scheme."""

    SKIP_PERC = 20

    ds = parse_ds("tests/data/ave-01.dat.gz", None, True)
    stats, report = ave(ds, SKIP_PERC)

    assert report == "31744/40497 rows"

    assert stats[0].nbins == [1024, 512, 256, 128, 64]
    assert stats[0].bsize == [31, 62, 124, 248, 496]
    assert stats[0].m == [
        -0.4995448147996472,
        -0.4995448147996472,
        -0.4995448147996472,
        -0.4995448147996472,
        -0.4995448147996472,
    ]
    assert stats[0].s == [
        0.0001743365336048138,
        0.0001804272766564555,
        0.00017649019401418475,
        0.00017824435864908882,
        0.0001582510738620892,
    ]
    assert stats[0].ds == [
        3.854211934119563e-06,
        5.643866677903565e-06,
        7.815117148541072e-06,
        1.1184045756749872e-05,
        1.409812617811892e-05,
    ]
    assert stats[1].nbins == stats[0].nbins
    assert stats[1].bsize == stats[0].bsize
    assert stats[1].m == [
        -7.249938210590978,
        -7.249938210590978,
        -7.249938210590978,
        -7.249938210590978,
        -7.249938210590978,
    ]
    assert stats[1].s == [
        0.00015487978745936192,
        0.00015935176762772726,
        0.00015796910259900911,
        0.00016085464180606504,
        0.00014464381807345806,
    ]
    assert stats[1].ds == [
        3.4240644392581373e-06,
        4.984612903577757e-06,
        6.994989435854652e-06,
        1.0092917878463464e-05,
        1.2885895484422392e-05,
    ]
    assert stats[2].nbins == stats[0].nbins
    assert stats[2].bsize == stats[0].bsize
    assert stats[2].m == [
        -7.749483020854335,
        -7.749483020854335,
        -7.749483020854335,
        -7.749483020854335,
        -7.749483020854335,
    ]
    assert stats[2].s == [
        6.354113302173723e-05,
        6.286498225846817e-05,
        6.125512011034933e-05,
        6.325707823701933e-05,
        5.849772523448627e-05,
    ]
    assert stats[2].ds == [
        1.4047600243962637e-06,
        1.966451997450092e-06,
        2.7124223092635907e-06,
        3.9691020955896445e-06,
        5.211391565073522e-06,
    ]
    assert stats[3].nbins == stats[0].nbins
    assert stats[3].bsize == stats[0].bsize
    assert stats[3].m == stats[1].m
    assert stats[3].s == stats[1].s
    assert stats[3].ds == stats[1].ds


def test_single_column():
    """Test a single-column averaging scheme."""

    SKIP_PERC = 20

    ds = parse_ds("tests/data/ave-01.dat.gz", [2], True)
    stats, report = ave(ds, SKIP_PERC)

    assert report == "31744/40497 rows"

    assert stats[0].nbins == [1024, 512, 256, 128, 64]
    assert stats[0].bsize == [31, 62, 124, 248, 496]
    assert stats[0].m == [
        -7.749483020854335,
        -7.749483020854335,
        -7.749483020854335,
        -7.749483020854335,
        -7.749483020854335,
    ]
    assert stats[0].s == [
        6.354113302173686e-05,
        6.286498225847002e-05,
        6.125512011035135e-05,
        6.325707823702418e-05,
        5.849772523449204e-05,
    ]
    assert stats[0].ds == [
        1.4047600243962557e-06,
        1.96645199745015e-06,
        2.71242230926368e-06,
        3.9691020955899495e-06,
        5.211391565074036e-06,
    ]
