"""Entrypoint, command-line interface to statistical functions."""

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


import sys

from modules.functionals import susceptibility
from modules.parser import build_parser
from modules.common import parse_ds
from modules.drivers import avs
from modules.drivers import ave
from modules.drivers import jck
from modules.print import PrintConfig
from modules.print import print_avs
from modules.print import print_ave
from modules.print import print_jck


__version__ = "1.2.5-1"


def main():
    """Implement main entrypoint."""
    parser = build_parser()
    args = parser.parse_args()

    if args.version:
        print(f"das v{__version__}")
        sys.exit(0)

    # converting to list of integers,
    # raises ValueError and terminates if invalid value
    if args.fields is not None:
        args.fields = [int(s) for s in args.fields.split(",")]
        numpy_fields = [(f - 1) for f in args.fields]
    else:
        numpy_fields = args.fields

    # parsing (common)
    data = parse_ds(args.file, numpy_fields, not args.quick)
    print_config = PrintConfig(args.fields, args.verbose, args.basic)

    if args.command == "avs":
        stats, report = avs(data, args.skip)
        print_avs(
            stats,
            report,
            print_config,
        )
    elif args.command == "ave":
        stats, actimes, report = ave(data, args.skip, args.actime)
        print_ave(
            stats,
            actimes,
            report,
            print_config,
        )
    elif args.command == "jck":
        stats, report = jck(data, args.skip, susceptibility)
        print_jck(
            stats,
            report,
            print_config,
        )


if __name__ == "__main__":
    main()
