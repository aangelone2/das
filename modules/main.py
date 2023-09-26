"""Entrypoint, command-line interface to statistical functions."""


import argparse
from rich.console import Console
from rich.table import Table

from modules.common import parse_ds
from modules.drivers import avs


console = Console()


def main():
    """Implement main entrypoint."""
    parser = argparse.ArgumentParser()

    parser.add_argument("file", help="file to analyze")
    parser.add_argument(
        "-f",
        "--fields",
        type=str,
        help="comma-separated, 1-indexed fields to analyze (default = all)",
        default=None,
    )
    parser.add_argument(
        "-q",
        "--quick",
        help="skip row integrity check",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="verbose output",
        action="store_true",
    )

    subp = parser.add_subparsers(dest="command")

    avs_parser = subp.add_parser(
        "avs",
        description="performs averaging without rebinning",
    )
    avs_parser.add_argument(
        "-s",
        "--skip",
        help="percentage (1-100) of rows to skip (default = 0)",
        type=int,
        default=0,
    )

    args = parser.parse_args()

    # converting to list of integers,
    # raises ValueError and terminates if invalid value
    if args.fields is not None:
        args.fields = [
            (int(s) - 1) for s in args.fields.split(",")
        ]

    # parsing (common)
    ds = parse_ds(args.file, args.fields, not args.quick)

    if args.command == "avs":
        stats, _ = avs(ds, args.skip)

        table = Table(box=None)
        table.add_column("column")
        table.add_column("mean")
        table.add_column("σ of mean")
        table.add_column("σ of σ of mean")

        cols = (
            range(len(stats))
            if args.fields is None
            else args.fields
        )

        for col, col_stats in zip(cols, stats):
            table.add_row(
                f"{col}",
                f'{col_stats["m"]:.11e}',
                f'{col_stats["s"]:.1e}',
                f'{col_stats["ds"]:.1e}',
            )

        console.print(table)


if __name__ == "__main__":
    main()
