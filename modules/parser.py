"""Utility module to build the parsers required by the main interface.

Functions
-----------------------
build_parser()
    Return the pre-built parser (with subparsers).
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


import argparse


def build_parser() -> argparse.ArgumentParser:
    """Return the pre-built parser (with subparsers).

    Returns
    -----------------------
    argparse.ArgumentParser
        The intialized parser.
    """
    # parent parser with shared options
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "-b",
        "--basic",
        help="simplified, parsing-friendly output formatting",
        action="store_true",
    )
    parent_parser.add_argument(
        "-f",
        "--fields",
        type=str,
        help="comma-separated, 1-indexed fields to analyze (default = all)",
        default=None,
    )
    parent_parser.add_argument(
        "-q",
        "--quick",
        help="skip row integrity check",
        action="store_true",
    )
    parent_parser.add_argument(
        "-v",
        "--verbose",
        help="verbose output",
        action="store_true",
    )
    parent_parser.add_argument(
        "-s",
        "--skip",
        help="percentage (1-100) of rows to skip (default = 0)",
        type=int,
        default=0,
    )
    parent_parser.add_argument("file", help="file to analyze")

    # main parser
    parser = argparse.ArgumentParser()
    subp = parser.add_subparsers(dest="command")

    _ = subp.add_parser(
        "avs",
        description="performs averages without rebinning",
        parents=[parent_parser],
    )

    return parser
