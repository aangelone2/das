"""Printing functions for formatted output.

Functions
-----------------------
print_avs()
    Print `avs` results in formatted way.
print_ave()
    Print `ave` results in formatted way.
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

from common import Stats


console = Console()


def print_avs(
    stats: list[Stats],
    report: str,
    fields: list[int] | None,
    verbose: bool,
    basic: bool,
) -> None:
    """Print `avs` results in formatted way.

    Parameters
    -----------------------
    stats : list[Stats]
        The first result from a call to avs()
    report : str
        The report string
    fields : list[int] | None
        The analyzed columns
    verbose : bool
        If True, prints the report information
    basic : bool
        If True, uses parse-friendly formatting
    """
    cols = (
        range(1, len(stats) + 1) if fields is None else fields
    )

    if not basic:
        if verbose:
            console.print(report)
            console.print()

        table = Table()
        table.add_column("column")
        table.add_column("mean")
        table.add_column("σ of mean")
        table.add_column("σ of σ of mean")

        for col, col_stats in zip(cols, stats):
            table.add_row(
                f"{col}",
                f"{col_stats.m:.11e}",
                f"{col_stats.s:.1e}",
                f"{col_stats.ds:.1e}",
            )

        console.print(table)
    else:
        if verbose:
            print(report)
            print()

        for col, col_stats in zip(cols, stats):
            print(
                f"{col}",
                f"{col_stats.m:.11e}",
                f"{col_stats.s:.1e}",
                f"{col_stats.ds:.1e}",
            )


def print_ave(
    stats: dict[int, list[Stats]],
    fields: list[int] | None,
    basic: bool,
) -> None:
    """Print `ave` results in formatted way.

    Parameters
    -----------------------
    stats : dict[int, list[Stats]]
        The result from a call to ave()
    fields : list[int] | None
        The analyzed columns
    basic : bool
        If True, uses parse-friendly formatting
    """
    cols = (
        range(1, len(stats) + 1) if fields is None else fields
    )

    if not basic:
        table = Table()
        table.add_column("column")
        table.add_column("bin number")
        table.add_column("mean")
        table.add_column("σ of mean")
        table.add_column("σ of σ of mean")

        for col, scaling in zip(cols, stats):
            for nbins, res in scaling.items():
                table.add_row(
                    f"{col}",
                    f"{nbins}",
                    f"{res.m:.11e}",
                    f"{res.s:.1e}",
                    f"{res.ds:.1e}",
                )

        console.print(table)
    else:
        for col, scaling in zip(cols, stats):
            for nbins, res in scaling.items():
                print(
                    f"{col}",
                    f"{nbins}",
                    f"{res.m:.11e}",
                    f"{res.s:.1e}",
                    f"{res.ds:.1e}",
                )
