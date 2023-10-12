"""Printing functions for formatted output.

Functions
-----------------------
print_avs()
    Print `avs` results in formatted way.
_print_fancy_ave()
    Low-level function, fancy printing of `ave` results.
_print_basic_ave()
    Low-level function, basic printing of `ave` results.
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


from typing import List
from typing import Optional
from dataclasses import dataclass

from rich.console import Console
from rich.table import Table

from modules.common import Stats
from modules.common import BinnedStats


console = Console()


@dataclass
class PrintConfig:
    """Common configuration for print functions.

    Attributes
    -----------------------
    fields : Optional[List[int]]
        The analyzed columns.
    verbose : bool
        If `True`, prints the report information.
    basic : bool
        If `True`, uses parse-friendly formatting.
    """

    fields: Optional[List[int]]
    verbose: bool
    basic: bool


def print_avs(
    stats: Stats,
    report: str,
    config: PrintConfig,
) -> None:
    """Print `avs` results in formatted way.

    Parameters
    -----------------------
    stats : Stats
        The first result from a call to `avs()`.
    report : str
        The report string.
    config : PrintConfig
        The printout configuration.
    """
    cols = (
        range(1, len(stats.m) + 1)
        if config.fields is None
        else config.fields
    )

    if not config.basic:
        if config.verbose:
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
        if config.verbose:
            print(report)
            print()

        for c, m, s in zip(cols, stats.m, stats.s):
            print(f"{c} {m:+.11e} {s:.1e}")


def _print_fancy_ave(
    stats: List[BinnedStats],
    actimes: List[float],
    report: str,
    config: PrintConfig,
) -> None:
    """Low-level function, fancy printing of `ave` results.

    Parameters
    -----------------------
    stats : List[BinnedStats]
        The result from a call to ave().
    actimes : List[float]
        List of the autocorrelation times (empty if not computed).
    report : str
        The report string.
    config : PrintConfig
        The printout configuration.
    """
    if config.verbose:
        console.print(report)
        console.print()

    table = Table()
    table.add_column("col")
    table.add_column("bins")
    table.add_column("binsize")
    table.add_column("mean")
    table.add_column("SEM")
    table.add_column("SE(SEM)")

    if actimes:
        table.add_column("actime")

        for col, scaling, t in zip(
            config.fields, stats, actimes
        ):
            for irow, (nb, bs, m, s, ds) in enumerate(
                zip(
                    scaling.nbins,
                    scaling.bsize,
                    scaling.m,
                    scaling.s,
                    scaling.ds,
                )
            ):
                table.add_row(
                    f"{col}",
                    f"{nb}",
                    f"{bs}",
                    f"{m:.11e}",
                    f"{s:.1e}",
                    f"{ds:.1e}",
                    f"{t:.1e}" if irow == 0 else "",
                )
            table.add_section()
    else:
        for col, scaling in zip(config.fields, stats):
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


def _print_basic_ave(
    stats: List[BinnedStats],
    actimes: List[float],
    report: str,
    config: PrintConfig,
) -> None:
    """Low-level function, basic printing of `ave` results.

    Parameters
    -----------------------
    stats : List[BinnedStats]
        The result from a call to ave().
    actimes : List[float]
        List of the autocorrelation times (empty if not computed).
    report : str
        The report string.
    config : PrintConfig
        The printout configuration.
    """
    if config.verbose:
        print(report)
        print()

    if actimes:
        for col, scaling, t in zip(
            config.fields, stats, actimes
        ):
            for irow, (nb, bs, m, s, ds) in enumerate(
                zip(
                    scaling.nbins,
                    scaling.bsize,
                    scaling.m,
                    scaling.s,
                    scaling.ds,
                )
            ):
                print(
                    f"{col} {nb:04d} {bs:04d} {m:+.11e} {s:.1e} {ds:.1e}",
                    f" {t:.1e}" if irow == 0 else "",
                )
    else:
        for col, scaling in zip(config.fields, stats):
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


def print_ave(
    stats: List[BinnedStats],
    actimes: List[float],
    report: str,
    config: PrintConfig,
) -> None:
    """Print `ave` results in formatted way.

    Parameters
    -----------------------
    stats : List[BinnedStats]
        The result from a call to ave().
    actimes : List[float]
        List of the autocorrelation times (empty if not computed).
    report : str
        The report string.
    config : PrintConfig
        The printout configuration.
    """
    # Setting column values
    config.fields = (
        range(1, len(stats) + 1)
        if config.fields is None
        else config.fields
    )

    if not config.basic:
        _print_fancy_ave(stats, actimes, report, config)
    else:
        _print_basic_ave(stats, actimes, report, config)


def print_jck(
    stats: BinnedStats,
    report: str,
    config: PrintConfig,
) -> None:
    """Print `jck` results in formatted way.

    Parameters
    -----------------------
    stats : BinnedStats
        The result from a call to jck().
    report : str
        The report string.
    config : PrintConfig
        The printout configuration.
    """
    if not config.basic:
        if config.verbose:
            report = report + f" :: fields {config.fields}"
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
        if config.verbose:
            report = report + f" :: fields {config.fields}"
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
