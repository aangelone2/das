"""Printing functions for formatted output.

Functions
-----------------------
print_avs()
    Print `avs` results in formatted way.
print_ave()
    Print `ave` results in formatted way.
print_jck()
    Print `jck` results in formatted way.
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


from rich.console import Console
from rich.table import Table

from modules.common import Stats
from modules.common import BinnedStats


console = Console()


def print_avs(
    stats: Stats,
    report: str,
    fields: list[int] | None,
    verbose: bool,
    basic: bool,
) -> None:
    """Print `avs` results in formatted way.

    Parameters
    -----------------------
    stats : Stats
        The first result from a call to `avs()`.
    report : str
        The report string.
    fields : list[int] | None
        The analyzed columns.
    verbose : bool
        If `True`, prints the report information.
    basic : bool
        If `True`, uses parse-friendly formatting.
    """
    cols = (
        range(1, len(stats.m) + 1)
        if fields is None
        else fields
    )

    if not basic:
        if verbose:
            console.print(report)
            console.print()

        table = Table()
        table.add_column("column")
        table.add_column("mean")
        table.add_column("SEM")

        for c, m, s in zip(cols, stats.m, stats.s):
            table.add_row(
                f"{c}",
                f"{m:.11e}",
                f"{s:.1e}",
            )

        console.print(table)
    else:
        if verbose:
            print(report)
            print()

        for c, m, s in zip(cols, stats.m, stats.s):
            print(f"{c} {m:+.11e} {s:.1e}")


def print_ave(
    stats: list[BinnedStats],
    report: str,
    fields: list[int] | None,
    verbose: bool,
    basic: bool,
) -> None:
    """Print `ave` results in formatted way.

    Parameters
    -----------------------
    stats : list[BinnedStats]
        The result from a call to ave().
    report : str
        The report string.
    fields : list[int] | None
        The analyzed columns.
    verbose : bool
        If `True`, prints the report information.
    basic : bool
        If `True`, uses parse-friendly formatting.
    """
    cols = (
        range(1, len(stats) + 1) if fields is None else fields
    )

    if not basic:
        if verbose:
            console.print(report)
            console.print()

        table = Table()
        table.add_column("col")
        table.add_column("bins")
        table.add_column("binsize")
        table.add_column("mean")
        table.add_column("SEM")
        table.add_column("SE(SEM)")

        for col, scaling in zip(cols, stats):
            for nb, bs, m, s, ds in zip(
                scaling.nbins,
                scaling.bsize,
                scaling.m,
                scaling.s,
                scaling.ds,
            ):
                table.add_row(
                    f"{col}",
                    f"{nb}",
                    f"{bs}",
                    f"{m:.11e}",
                    f"{s:.1e}",
                    f"{ds:.1e}",
                )
            table.add_section()

        console.print(table)
    else:
        if verbose:
            print(report)
            print()

        for col, scaling in zip(cols, stats):
            for nb, bs, m, s, ds in zip(
                scaling.nbins,
                scaling.bsize,
                scaling.m,
                scaling.s,
                scaling.ds,
            ):
                print(
                    f"{col} {nb:04d} {bs:04d} {m:+.11e} {s:.1e} {ds:.1e}"
                )


def print_jck(
    stats: BinnedStats,
    report: str,
    fields: list[int] | None,
    verbose: bool,
    basic: bool,
) -> None:
    """Print `jck` results in formatted way.

    Parameters
    -----------------------
    stats : BinnedStats
        The result from a call to jck().
    report : str
        The report string.
    fields : list[int] | None
        The analyzed columns.
    verbose : bool
        If `True`, prints the report information.
    basic : bool
        If `True`, uses parse-friendly formatting.
    """
    if not basic:
        if verbose:
            report = report + f" :: fields {fields}"
            console.print(report)
            console.print()

        table = Table()
        table.add_column("bins")
        table.add_column("binsize")
        table.add_column("mean")
        table.add_column("SEM")
        table.add_column("SE(SEM)")

        for nb, bs, m, s, ds in zip(
            stats.nbins,
            stats.bsize,
            stats.m,
            stats.s,
            stats.ds,
        ):
            table.add_row(
                f"{nb}",
                f"{bs}",
                f"{m:.11e}",
                f"{s:.1e}",
                f"{ds:.1e}",
            )

        console.print(table)
    else:
        if verbose:
            report = report + f" :: fields {fields}"
            print(report)
            print()

        for nb, bs, m, s, ds in zip(
            stats.nbins,
            stats.bsize,
            stats.m,
            stats.s,
            stats.ds,
        ):
            print(
                f"{nb:04d} {bs:04d} {m:+.11e} {s:.1e} {ds:.1e}"
            )
