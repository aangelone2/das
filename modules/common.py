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
Stats
    Result class for get_stats().
"""

# Copyright (c) 2023 Adriano Angelone
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the
# Software.
#
# This file is part of das.
#
# This file may be used under the terms of the GNU General
# Public License version 3.0 as published by the Free Software
# Foundation and appearing in the file LICENSE included in the
# packaging of this file.  Please review the following
# information to ensure the GNU General Public License version
# 3.0 requirements will be met:
# http://www.gnu.org/copyleft/gpl.html.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import os
from math import sqrt
from dataclasses import dataclass

import numpy as np


# MAX AND MIN NUM OF BINS TO CONSIDER WHEN BINNING
MAXBINS = 1024
MINBINS = 64


class ParsingError(Exception):
    """Subclassed exception for errors in dataset parsing."""


class TailoringError(Exception):
    """Subclassed exception for errors in dataset tailoring."""


@dataclass
class Stats:
    """Result class for get_stats().

    Attributes
    -----------------------
    m : list[float]
        Column averages.
    s : list[float]
        Column standard errors of the mean.
    ds : list[float]
        Column standard errors of `s`.
    total : list[float]
        Column sums.
    """

    m: list[float]
    s: list[float]
    ds: list[float]
    total: list[float]


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
        A 2D array storing the parsed dataset

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
                ndmin=2,
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
                ndmin=2,
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
    ds: np.array, skip_perc: int = 0, nbins: int | None = None
) -> np.array:
    """Remove rows from 2D array.

    Parameters
    -----------------------
    ds : np.array
        The dataset to tailor
    skip_perc : float, default = 0.0
        Percentage of rows to skip
    nbins : int | None, default = None
        If not None, will skip additional rows to allow this
        number of identical bins

    Returns
    -----------------------
    np.array
        The tailored array

    Raises
    -----------------------
    - TailoringError if `nbins` set and not enough rows left
    """
    rows = ds.shape[0]

    skip = int((skip_perc / 100.0) * rows)
    keep = rows - skip

    if nbins is not None:
        if nbins > keep:
            raise TailoringError("insufficient rows left")

        keep -= keep % nbins
        skip = rows - keep

    return ds[skip:]


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
    if ds.shape[0] < nbins:
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


def get_stats(ds: np.array) -> Stats:
    """Compute statistical observables for dataset.

    Parameters
    -----------------------
    ds : np.array
        The dataset to analyze

    Returns
    -----------------------
    Stats
        Stats object with column statistical summary
    """
    N = ds.shape[0]

    res = Stats(m=[], s=[], ds=[], total=[])
    for col in ds.T:
        res.m.append(col.mean())
        res.s.append(col.std(ddof=1) / sqrt(N))
        res.ds.append(res.s[-1] / sqrt(2.0 * (N - 1)))
        res.total.append(col.sum())

    return res
