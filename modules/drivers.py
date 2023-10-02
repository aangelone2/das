"""High-level drivers using the basic functions.

Functions
-----------------------
avs()
    Compute simple average, SEMs, and SE(SEM)s of a 2D array by
    columns.
ave()
    Compute binsize scaling of averages, SEMs, and SE(SEM)s of
    a 2D array by columns.
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


import numpy as np

from modules.common import MAXBINS
from modules.common import MINBINS
from modules.common import Stats
from modules.common import BinnedStats
from modules.common import drop_rows
from modules.common import rebin
from modules.common import get_stats


def avs(ds: np.array, skip_perc: int) -> (Stats, str):
    """Compute simple average, SEMs, and SE(SEM)s of a 2D array by columns.

    Parameters
    -----------------------
    ds : np.array
        The 2D array to parse.
    skip_perc : int
        The percentage (1-100) of rows to skip.

    Returns
    -----------------------
    (Stats, str)
        - Stats object with column statistics.
        - String carrying additional information.
    """
    rows = ds.shape[0]

    ds = drop_rows(ds, skip_perc, nbins=None)
    keep = ds.shape[0]

    report = f"{keep}/{rows} rows"
    return (get_stats(ds), report)


def ave(
    ds: np.array, skip_perc: int
) -> (list[BinnedStats], str):
    """Compute binsize scaling of averages, SEMs, and SE(SEM)s of a 2D array by columns.

    Parameters
    -----------------------
    ds : np.array
        The 2D array to parse.
    skip_perc : int
        The percentage (1-100) of rows to skip.

    Returns
    -----------------------
    (list[BinnedStats], str)
        - List of `BinnedStats` objects, 1 per column.
        - String carrying additional information.
    """
    rows = ds.shape[0]
    ds = drop_rows(ds, skip_perc, nbins=MAXBINS)
    keep = ds.shape[0]

    nbins = MAXBINS
    bsize = keep // nbins
    ds = rebin(ds, nbins=nbins)
    cols = ds.shape[1]

    res = [
        BinnedStats(
            nbins=[], bsize=[], m=[], s=[], ds=[], total=[]
        )
        for _ in range(cols)
    ]
    while nbins >= MINBINS:
        buffer = get_stats(ds)

        for r, m, s, d, t in zip(
            res, buffer.m, buffer.s, buffer.ds, buffer.total
        ):
            r.nbins.append(nbins)
            r.bsize.append(bsize)
            r.m.append(m)
            r.s.append(s)
            r.ds.append(d)
            r.total.append(t)

        nbins //= 2
        bsize *= 2
        ds = rebin(ds, nbins=nbins)

    report = f"{keep}/{rows} rows"
    return (res, report)
