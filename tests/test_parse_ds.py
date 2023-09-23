"""Test module for parse_ds() function."""

import numpy as np
import pytest

from modules.common import ParsingError
from modules.common import parse_ds


def test_missing_file():
    """Testing parsing of nonexistent file."""

    with pytest.raises(ParsingError):
        _ = parse_ds("tests/data/missing.dat", None, True)


def test_empty_lines():
    """Testing parsing of file with empty lines."""

    ds = parse_ds("tests/data/empty_lines.dat", None, True)
    assert ds.size == np.array([[1, 2, 3, 4], [5, 6, 7, 8]])


def test_empty_column():
    """Testing parsing of file with missing values."""

    # missing value in last row, column 2

    # parsing all columns, testing colnum
    with pytest.raises(ValueError):
        ds = parse_ds(
            "tests/data/empty_column.dat",
            None,
            colnum_test=True,
        )

    # only parsing cols [0,1], testing colnum
    ds = parse_ds(
        "tests/data/empty_column.dat", [0, 1], colnum_test=True
    )
    assert ds.size == np.array([[1, 2], [5, 6], [1, 2]])

    # parsing columns [2,4], testing colnum
    with pytest.raises(ValueError):
        ds = parse_ds(
            "tests/data/empty_column.dat",
            [2, 4],
            colnum_test=True,
        )

    # parsing all columns, NOT testing colnum
    with pytest.raises(ValueError):
        ds = parse_ds(
            "tests/data/empty_column.dat",
            None,
            colnum_test=False,
        )

    # only parsing cols [0,1], NOT testing colnum
    ds = parse_ds(
        "tests/data/empty_column.dat",
        [0, 1],
        colnum_test=False,
    )
    assert ds.size == np.array([[1, 2], [5, 6], [1, 2]])

    # parsing columns [2,4], NOT testing colnum
    with pytest.raises(ValueError):
        ds = parse_ds(
            "tests/data/empty_column.dat",
            [2, 4],
            colnum_test=False,
        )
