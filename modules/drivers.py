"""High-level drivers using the basic functions.

Functions
-----------------------
avs()
    Compute simple average of a dataset by columns.
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

from modules.common import drop_rows
from modules.common import get_stats


def avs(
    ds: np.array, skip_perc: float
) -> (list[dict[str, float]], str):
    """Compute simple average of a dataset by columns.

    Parameters
    -----------------------
    ds : np.array
        The dataset to parse
    skip_perc : float
        The percentage of rows to skip

    Returns
    -----------------------
    (list[dict[str, float]], str)
        - (mean, std, error on std) for each column (keys: (m, s, ds))
        - String carrying additional information
    """
    rows = ds.shape[0]

    ds = drop_rows(ds, skip_perc, power2=False)
    keep = ds.shape[0]

    report = f"{keep}/{rows} rows :: {keep} bins"

    stats = get_stats(ds)
    for col_res in stats:
        del col_res["sum"]

    return (stats, report)
