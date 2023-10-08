"""High-level drivers using the basic functions.

Functions
-----------------------
avs()
    Compute simple average, SEMs, and SE(SEM)s of a 2D array by
    columns.
ave()
    Compute binsize scaling of averages, SEMs, and SE(SEM)s of
    a 2D array by columns.
jck()
    Compute jackknife estimate for error of passed functional.
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


from typing import Callable
import numpy as np

from modules.common import MAXBINS
from modules.common import MINBINS
from modules.common import Stats
from modules.common import BinnedStats
from modules.common import drop_rows
from modules.common import rebin
from modules.common import get_stats


def avs(data: np.array, skip_perc: int) -> (Stats, str):
    """Compute simple average, SEMs, and SE(SEM)s of a 2D array by columns.

    Parameters
    -----------------------
    data : np.array
        The 2D array to analyze.
    skip_perc : int
        The percentage (1-100) of rows to skip.

    Returns
    -----------------------
    (Stats, str)
        - Stats object with column statistics.
        - String carrying additional information.
    """
    rows = data.shape[0]
    data = drop_rows(data, skip_perc, nbins=None)
    keep = data.shape[0]

    report = f"{keep}/{rows} rows"

    return (get_stats(data), report)


def ave(
    data: np.array, skip_perc: int
) -> (list[BinnedStats], str):
    """Compute binsize scaling of averages, SEMs, and SE(SEM)s of a 2D array by columns.

    Parameters
    -----------------------
    data : np.array
        The 2D array to analyze.
    skip_perc : int
        The percentage (1-100) of rows to skip.

    Returns
    -----------------------
    (list[BinnedStats], str)
        - List of `BinnedStats` objects, 1 per column.
        - String carrying additional information.
    """
    rows = data.shape[0]
    data = drop_rows(data, skip_perc, nbins=MAXBINS)
    keep = data.shape[0]

    report = f"{keep}/{rows} rows"

    nbins = MAXBINS
    bsize = keep // nbins
    data = rebin(data, nbins=nbins)

    cols = data.shape[1]
    res = [
        BinnedStats(nbins=[], bsize=[], m=[], s=[], ds=[])
        for _ in range(cols)
    ]

    while nbins >= MINBINS:
        buffer = get_stats(data)

        for r, m, s, d in zip(
            res, buffer.m, buffer.s, buffer.ds
        ):
            r.nbins.append(nbins)
            r.bsize.append(bsize)
            r.m.append(m)
            r.s.append(s)
            r.ds.append(d)

        nbins //= 2
        bsize *= 2
        data = rebin(data, nbins=nbins)

    return (res, report)


def jck(data: np.array, skip_perc: int, func: Callable):
    """Compute jackknife estimate for error of passed functional.

    See `modules.functionals` for blueprint of acceptable
    functionals.

    Parameters
    -----------------------
    data : np.array
        The 2D array to analyze.
    skip_perc : int
        The percentage (1-100) of rows to skip.
    func : Callable
        Functional used to compute values and pseudovalues.

    Returns
    -----------------------
    (BinnedStats, str)
        - `BinnedStats` objects with statistical information.
        - String carrying additional information.
    """
    rows = data.shape[0]
    data = drop_rows(data, skip_perc, nbins=MAXBINS)
    keep = data.shape[0]

    report = f"{keep}/{rows} rows"

    nbins = MAXBINS
    bsize = keep // nbins
    data = rebin(data, nbins=nbins)

    res = BinnedStats(nbins=[], bsize=[], m=[], s=[], ds=[])

    while nbins >= MINBINS:
        sums = data.sum(axis=0)
        # full value
        val = func(sums[0] / nbins, sums[1] / nbins)

        # vector pseudo-averages
        ps_ave_0 = (sums[0] - data[:, 0]) / (nbins - 1)
        ps_ave_1 = (sums[1] - data[:, 1]) / (nbins - 1)
        # vector of pseudovalues
        ps_val = nbins * val - (nbins - 1) * func(
            ps_ave_0, ps_ave_1
        )

        # Reshaping necessary
        ps_val = ps_val.reshape((ps_val.shape[0], 1))
        buffer = get_stats(ps_val)

        res.nbins.append(nbins)
        res.bsize.append(bsize)
        res.m.append(*buffer.m)
        res.s.append(*buffer.s)
        res.ds.append(*buffer.ds)

        nbins //= 2
        bsize *= 2
        data = rebin(data, nbins=nbins)

    return (res, report)
