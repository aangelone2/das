"""Entrypoint, command-line interface to statistical functions."""


import argparse

from common import parse_ds
from avs import avs


def main():
    """Implement main entrypoint."""
    parser = argparse.ArgumentParser()

    parser.add_argument("file", help="file to analyze")
    parser.add_argument(
        "-f",
        "--fields",
        help="comma-separated columns to average (default = all)",
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
        "-c",
        "--compatibility",
        help="use a power of 2 of points for compatibility with ave",
        action="store_true",
    )
    avs_parser.add_argument(
        "-s",
        "--skip",
        help="percentage of rows to skip (default = 0.0)",
        type=float,
        default=0.0,
    )

    args = parser.parse_args()

    # parsing (common)
    ds = parse_ds(args.file, args.fields, not args.quick)

    if args.command == "avs":
        avs(ds, args.skip, args.compatibility, args.verbose)


if __name__ == "__main__":
    main()
