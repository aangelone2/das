"""Test module for parse_ds() function."""


import numpy as np
import pytest

from modules.common import ParsingError
from modules.common import parse_ds


def test_missing_file():
    """Testing parsing of nonexistent file."""

    with pytest.raises(ParsingError) as err:
        _ = parse_ds("tests/data/missing.dat", None, True)
    assert str(err.value) == "file does not exist"


def test_empty_lines():
    """Testing parsing of file with empty lines."""

    ds = parse_ds("tests/data/pd-01-empty_lines.dat", None, True)
    assert np.array_equal(ds, np.array([[1, 2, 3, 4], [5, 6, 7, 8]]))


def test_empty_column():
    """Testing parsing of file with missing values."""

    # missing value row 3, column 2

    # parsing all columns, testing colnum
    with pytest.raises(ParsingError) as err:
        ds = parse_ds(
            "tests/data/pd-02-empty_column.dat",
            None,
            colnum_test=True,
        )
    assert (
        str(err.value)
        == "the number of columns changed from 4 to 3 at row 3; use `usecols` to select a subset and avoid this error"
    )

    # only parsing cols [0,1], testing colnum
    with pytest.raises(ParsingError) as err:
        ds = parse_ds(
            "tests/data/pd-02-empty_column.dat",
            [0, 1],
            colnum_test=True,
        )
    assert (
        str(err.value)
        == "the number of columns changed from 4 to 3 at row 3; use `usecols` to select a subset and avoid this error"
    )

    # parsing columns [1,3], testing colnum
    with pytest.raises(ParsingError) as err:
        ds = parse_ds(
            "tests/data/pd-02-empty_column.dat",
            [1, 3],
            colnum_test=True,
        )
    assert (
        str(err.value)
        == "the number of columns changed from 4 to 3 at row 3; use `usecols` to select a subset and avoid this error"
    )

    # parsing all columns, NOT testing colnum
    with pytest.raises(ParsingError) as err:
        ds = parse_ds(
            "tests/data/pd-02-empty_column.dat",
            None,
            colnum_test=False,
        )
    assert (
        str(err.value)
        == "the number of columns changed from 4 to 3 at row 3; use `usecols` to select a subset and avoid this error"
    )

    # only parsing cols [0,1], NOT testing colnum
    # should pass (missing column not within parsed span)
    ds = parse_ds(
        "tests/data/pd-02-empty_column.dat",
        [0, 1],
        colnum_test=False,
    )
    assert np.array_equal(ds, np.array([[1, 2], [5, 6], [1, 2]]))

    # parsing columns [1,3], NOT testing colnum
    with pytest.raises(ParsingError) as err:
        ds = parse_ds(
            "tests/data/pd-02-empty_column.dat",
            [1, 3],
            colnum_test=False,
        )
    assert str(err.value) == "invalid column index 3 at row 3 with 3 columns"


def test_missing_column():
    """Testing parsing of file without requested column."""

    # testing colnum
    with pytest.raises(ParsingError) as err:
        ds = parse_ds(
            "tests/data/pd-03-complete.dat",
            [3, 4],
            colnum_test=True,
        )
    assert str(err.value) == "index 4 is out of bounds for axis 1 with size 4"

    # NOT testing colnum
    with pytest.raises(ParsingError) as err:
        ds = parse_ds(
            "tests/data/pd-03-complete.dat",
            [3, 4],
            colnum_test=False,
        )
    assert str(err.value) == "invalid column index 4 at row 1 with 4 columns"

    # proper parsing, 1 column
    ds = parse_ds("tests/data/pd-03-complete.dat", [2], colnum_test=False)
    assert np.array_equal(
        ds,
        np.array(
            [
                [
                    3,
                ],
                [
                    7,
                ],
                [
                    3,
                ],
            ]
        ),
    )

    # proper parsing, 2 columns
    ds = parse_ds(
        "tests/data/pd-03-complete.dat",
        [1, 2],
        colnum_test=False,
    )
    assert np.array_equal(ds, np.array([[2, 3], [6, 7], [2, 3]]))


def test_single_column():
    """Testing parsing of a single-column file."""

    ds = parse_ds(
        "tests/data/pd-04-single_column.dat",
        None,
        colnum_test=True,
    )
    assert np.array_equal(
        ds,
        np.array(
            [
                [
                    2,
                ],
                [
                    6,
                ],
                [
                    2,
                ],
            ]
        ),
    )

    # setting 0th column
    ds = parse_ds(
        "tests/data/pd-04-single_column.dat",
        [0],
        colnum_test=True,
    )
    assert np.array_equal(
        ds,
        np.array(
            [
                [
                    2,
                ],
                [
                    6,
                ],
                [
                    2,
                ],
            ]
        ),
    )

    # filtering bigger file
    ds = parse_ds("tests/data/pd-03-complete.dat", [1], colnum_test=True)
    assert np.array_equal(
        ds,
        np.array(
            [
                [
                    2,
                ],
                [
                    6,
                ],
                [
                    2,
                ],
            ]
        ),
    )


def test_commented():
    """Testing file with internal commented lines."""

    ds = parse_ds(
        "tests/data/pd-05-commented.dat",
        None,
        colnum_test=False,
    )
    assert np.array_equal(
        ds,
        np.array([[1, 2, 3, 4], [5, 6, 7, 8], [1, 2, 3, 4]]),
    )


def test_empty():
    """Testing file with internal and final empty lines, and spurious spaces."""

    # with colnum_test
    ds = parse_ds("tests/data/pd-06-empty.dat", None, colnum_test=True)
    assert np.array_equal(
        ds,
        np.array([[1, 2, 3, 4], [5, 6, 7, 8], [1, 2, 3, 4]]),
    )

    # without colnum_test
    ds = parse_ds("tests/data/pd-06-empty.dat", None, colnum_test=False)
    assert np.array_equal(
        ds,
        np.array([[1, 2, 3, 4], [5, 6, 7, 8], [1, 2, 3, 4]]),
    )


def test_spurious_field():
    """Testing file with spurious (non-numerical) field."""

    # with colnum_test
    with pytest.raises(ParsingError) as err:
        _ = parse_ds("tests/data/pd-07-spurious.dat", None, colnum_test=True)
    assert str(err.value) == "could not convert string 'ab' to float64 at row 1, column 3."

    # without colnum_test
    with pytest.raises(ParsingError) as err:
        _ = parse_ds("tests/data/pd-07-spurious.dat", None, colnum_test=False)
    assert str(err.value) == "could not convert string 'ab' to float64 at row 1, column 3."
