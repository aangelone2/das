"""Common utilities, used by several higher-level scripts.

Functions
-----------------------
parse_ds()
    Parse a 2D data set from a file.
drop_rows()
    Remove rows from 2D array.
rebin()
    Rebins a 2D array with perfect shape assumed.

Classes
-----------------------
ParsingError
    Subclassed exception for errors in dataset parsing.
TailoringError
    Subclassed exception for errors in dataset tailoring.
"""


import os
import math

import numpy as np


# MAX AND MIN NUM OF BINS TO CONSIDER WHEN BINNING
MAXBINS = 1024
MINBINS = 64


class ParsingError(Exception):
    """Subclassed exception for errors in dataset parsing."""


class TailoringError(Exception):
    """Subclassed exception for errors in dataset tailoring."""


def parse_df(
    file: str,
    fields: list[int] | None = None,
    colnum_test: bool = False,
) -> np.array:
    """Parse a 2D data set from a file.

    Ignores blank lines, does not accept non-commented headers.
    Raises error if empty column read.

    Parameters
    -----------------------
    file : str
        The file to open for reading
    fields : list[int] | None, default = None
        List of fields to parse (0-indexed), all fields if None
    colnum_test: bool, default = False
        If True, checks if all rows have the same number of
        columns

    Returns
    -----------------------
    np.array
        A 2D array (may be 1-column) with the parsed dataset

    Raises
    -----------------------
    - ParsingError if file not found
    """
    # FIXME exceptions (fields not found,
    # field number too large, ...)

    if not os.path.isfile(file):
        raise ParsingError("file does not exist")

    if not colnum_test:
        # only take selected columns, others ignored
        # (unless an empty column in or between the selected,
        # then an exception is raised)
        dataset = np.loadtxt(
            file,
            comments="#",
            dtype=np.float64,
            usecols=fields,
        )
    else:
        # get all columns
        dataset = np.loadtxt(
            file, comments="#", dtype=np.float64, usecols=None
        )

        if fields is not None:
            dataset = dataset[:, fields]

    return dataset


def drop_rows(
    ds: np.array, perc: float = 0.0, power2: bool = False
) -> np.array:
    """Remove rows from 2D array.

    Parameters
    -----------------------
    ds : np.array
        The array to tailor
    perc : float, default = 0.0
        Percentage of rows to skip
    power2 : bool, default = False
        After `perc`, skips enough to leave the closest power
        of 2 if True

    Returns
    -----------------------
    np.array
        The tailored array

    Raises
    -----------------------
    - TailoringError if `power2` set and not enough rows left
    """
    rows = ds.shape[0]

    skip = int((perc / 100.0) * rows)
    keep = rows - skip

    if power2:
        if keep < 2:
            raise TailoringError("insufficient number of rows")

        keep = 2 ** (math.frexp(keep)[1] - 1)
        skip = rows - keep

    return np.delete(ds, range(skip), axis=0)


def rebin(ds: np.array, nbins: int) -> np.array:
    """Rebins a 2D array with perfect shape assumed.

    Parameters
    -----------------------
    ds : np.array
        The array to rebin
    nbins : int
        Number of requested bins

    Returns
    -----------------------
    np.array
        The rebinned array

    Raises
    -----------------------
    - TailoringError if insufficient rows for binning
    - TailoringError if leftover rows after binning
    """
    if ds.shape[0] > nbins:
        raise TailoringError("insufficient rows for binning")

    if ds.shape[0] % nbins != 0:
        raise TailoringError("leftover rows in binning")

    size = ds.shape[0] // nbins
    ds2 = np.ndarray((nbins, ds.shape[1]))

    for ib in range(nbins):
        ds2[ib] = ds[(ib * size) : ((ib + 1) * size)].mean(
            axis=0
        )
    return ds2
