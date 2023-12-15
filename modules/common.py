"""Common utilities, used by several higher-level scripts.

Functions
-----------------------
parse_ds()
    Parse a 2D array from a file.
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
    Result class for `get_stats()`.
BinnedStats
    Results of bin number scaling (single column).
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
from typing import Optional

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
    """Result class for `get_stats()`.

    Attributes
    -----------------------
    m : list[float]
        Column averages.
    s : list[float]
        Column SEMs.
    ds : list[float]
        Column SE(SEM)s.
    """

    m: list[float]
    s: list[float]
    ds: list[float]


@dataclass
class BinnedStats:
    """Results of bin number scaling (single column).

    Attributes
    -----------------------
    nbins: list[int]
        List of bin numbers.
    bsize: list[int]
        List of binsizes.
    m : list[float]
        Average per binsize.
    s : list[float]
        SEM per binsize.
    ds : list[float]
        SE(SEM) per binsize.
    """

    nbins: list[int]
    bsize: list[int]
    m: list[float]
    s: list[float]
    ds: list[float]


def parse_ds(
    file: str,
    fields: Optional[list[int]] = None,
    colnum_test: bool = False,
) -> np.ndarray:
    """Parse a 2D array from a file.

    - Empty and commented (`#`) lines are skipped.
    - Does not accept non-commented headers.

    Parameters
    -----------------------
    file : str
        Path to the file to open for reading.
    fields : Optional[list[int]], default = None
        List of fields to parse (0-indexed), all fields if
        `None`.
    colnum_test: bool, default = False
        If `True`, checks if all rows have the same number of
        columns.

    Returns
    -----------------------
    np.ndarray
        A 2D array storing the parsed dataset.

    Raises
    -----------------------
    ParsingError
        If file not found.
    ParsingError
        If any field is missing and `colnum_test is True`.
    ParsingError
        If missing field is among or between those in `fields`,
        regardless of `colnum_test`.
    ParsingError
        If requested column(s) do not exist.
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
    data: np.ndarray,
    skip_perc: int = 0,
    nbins: Optional[int] = None,
) -> np.ndarray:
    """Remove rows from 2D array.

    Parameters
    -----------------------
    data : np.ndarray
        The dataset to tailor.
    skip_perc : int, default = 0
        Percentage (1-100) of rows to skip.
    nbins : Optional[int], default = None
        If not `None`, will skip additional rows to allow this
        number of identical bins.

    Returns
    -----------------------
    np.ndarray
        The tailored array.

    Raises
    -----------------------
    ValueError
        If `skip_perc` not in [0, 100].
    TailoringError
        If `nbins` set and not enough rows left.
    """
    rows = data.shape[0]

    if not 0 <= skip_perc <= 100:
        raise ValueError("invalid skip percentage")

    skip = int((skip_perc / 100.0) * rows)
    keep = rows - skip

    if nbins is not None:
        if nbins > keep:
            raise TailoringError("insufficient rows left")

        keep -= keep % nbins
        skip = rows - keep

    return data[skip:]


def rebin(data: np.ndarray, nbins: int) -> np.ndarray:
    """Rebin a 2D array with perfect shape assumed.

    Parameters
    -----------------------
    data : np.ndarray
        The dataset to rebin.
    nbins : int
        Number of requested bins.

    Returns
    -----------------------
    np.ndarray
        The rebinned array.

    Raises
    -----------------------
    TailoringError
        If insufficient rows for binning.
    TailoringError
        If leftover rows after binning.
    """
    if data.shape[0] < nbins:
        raise TailoringError("insufficient rows for binning")

    if data.shape[0] % nbins != 0:
        raise TailoringError("leftover rows in binning")

    size = data.shape[0] // nbins
    data2 = np.ndarray((nbins, data.shape[1]))

    for ib in range(nbins):
        data2[ib] = data[(ib * size) : ((ib + 1) * size)].mean(axis=0)
    return data2


def get_stats(data: np.ndarray) -> Stats:
    """Compute statistical observables for dataset.

    Parameters
    -----------------------
    data : np.ndarray
        The dataset to analyze.

    Returns
    -----------------------
    Stats
        Stats object with column statistical summary.
    """
    N = data.shape[0]

    res = Stats(m=[], s=[], ds=[])
    for col in data.T:
        res.m.append(col.mean())
        res.s.append(col.std(ddof=1) / sqrt(N))
        res.ds.append(res.s[-1] / sqrt(2.0 * (N - 1)))

    return res
