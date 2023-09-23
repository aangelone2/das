"""Common utilities, used by several higher-level scripts.

Functions
-----------------------
parse_ds()
    Parse a 2D data set from a file.
drop_rows()
    Remove rows from 2D array.
rebin()
    Rebin a 2D array with perfect shape assumed.
get_stats()
    Compute statistical observables for dataset.

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


def parse_ds(
    file: str,
    fields: list[int] | None = None,
    colnum_test: bool = False,
) -> np.array:
    """Parse a 2D data set from a file.

    - Empty and commented (#) lines are skipped
    - Does not accept non-commented headers

    Parameters
    -----------------------
    file : str
        The file to open for reading
    fields : list[int] | None, default = None
        List of fields to parse (0-indexed), all fields if None
    colnum_test: bool, default = False
        If True, checks if all rows have the same number of columns

    Returns
    -----------------------
    np.array
        A 2D array (1D if only 1 column) storing the parsed dataset

    Raises
    -----------------------
    - ParsingError if file not found
    - ParsingError if missing field and `colnum_test is True`
      or missing field is among or between those in `fields`
    - ParsingError if requested column(s) do not exist
    """
    if not os.path.isfile(file):
        raise ParsingError("file does not exist")

    if not colnum_test:
        # only take selected columns, others ignored
        # (unless an empty column in or between the selected,
        # then an exception is raised)
        try:
            dataset = np.loadtxt(
                file,
                comments="#",
                dtype=np.float64,
                usecols=fields,
            )
        except ValueError as err:
            raise ParsingError(err) from err
    else:
        # get all columns
        try:
            dataset = np.loadtxt(
                file,
                comments="#",
                dtype=np.float64,
                usecols=None,
            )
        except ValueError as err:
            raise ParsingError(err) from err

        try:
            if fields is not None:
                dataset = dataset[:, fields]
        except IndexError as err:
            raise ParsingError(err) from err

    return dataset


def drop_rows(
    ds: np.array, skip_perc: float = 0.0, power2: bool = False
) -> np.array:
    """Remove rows from 2D array.

    Parameters
    -----------------------
    ds : np.array
        The dataset to tailor
    skip_perc : float, default = 0.0
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

    skip = int((skip_perc / 100.0) * rows)
    keep = rows - skip

    if power2:
        if keep < 2:
            raise TailoringError("insufficient number of rows")

        keep = 2 ** (math.frexp(keep)[1] - 1)
        skip = rows - keep

    return np.delete(ds, range(skip), axis=0)


def rebin(ds: np.array, nbins: int) -> np.array:
    """Rebin a 2D array with perfect shape assumed.

    Parameters
    -----------------------
    ds : np.array
        The dataset to rebin
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


def get_stats(ds: np.array) -> dict[str, float]:
    """Compute statistical observables for dataset.

    Parameters
    -----------------------
    ds : np.array
        The dataset to analyze

    Returns
    -----------------------
    list[dict[str, float]]
        Dict of stats for each column, keys:
          - m (average)
          - s (standard deviation of the mean)
          - ds (standard deviation of s)
          - sum (sum)

    Raises
    -----------------------
    - TailoringError if insufficient rows (< MINBINS)
    """
    res = []
    N = ds.shape[0]

    if N < MINBINS:
        raise TailoringError("insufficient number of rows")

    for col in range(ds.shape[1]):
        data = ds[:, col]

        m = data.mean()
        s = m.std(ddof=1) / math.sqrt(N)
        ds = s / math.sqrt(2.0 * (N - 1))

        sm = data.sum()

        res.append({"m": m, "s": s, "ds": ds, "sum": sm})

    return res
