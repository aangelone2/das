"""Test module for parse_ds() function."""

import numpy as np
import pytest

from modules.common import ParsingError
from modules.common import parse_ds


def test_missing_file():
    """Testing parsing of nonexistent file."""

    with pytest.raises(ParsingError) as err:
        _ = parse_ds("tests/data/missing.dat", None, True)
        assert err == "file does not exist"


def test_empty_lines():
    """Testing parsing of file with empty lines."""

    ds = parse_ds("tests/data/empty_lines.dat", None, True)
    assert np.array_equal(
        ds, np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    )


def test_empty_column():
    """Testing parsing of file with missing values."""

    # missing value row 3, column 2

    # parsing all columns, testing colnum
    with pytest.raises(ParsingError) as err:
        ds = parse_ds(
            "tests/data/empty_column.dat",
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
            "tests/data/empty_column.dat",
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
            "tests/data/empty_column.dat",
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
            "tests/data/empty_column.dat",
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
        "tests/data/empty_column.dat",
        [0, 1],
        colnum_test=False,
    )
    assert np.array_equal(
        ds, np.array([[1, 2], [5, 6], [1, 2]])
    )

    # parsing columns [1,3], NOT testing colnum
    with pytest.raises(ParsingError) as err:
        ds = parse_ds(
            "tests/data/empty_column.dat",
            [1, 3],
            colnum_test=False,
        )
    assert (
        str(err.value)
        == "invalid column index 3 at row 3 with 3 columns"
    )
