"""The command line: tip BILL [--percent P] [--people N] [-v]."""
import argparse
import logging
import sys

from tipcalc import split_bill

logger = logging.getLogger(__name__)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="tip", description="Split a bill, tip included.")
    parser.add_argument("bill", type=float,
                        help="the bill in dollars")
    parser.add_argument("-p", "--percent", type=float, default=15,
                        help="tip percentage (default: %(default)s)")
    parser.add_argument("-n", "--people", type=int, default=1,
                        help="people sharing (default: %(default)s)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="explain what the program is doing")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s:%(name)s: %(message)s")
    logger.debug("arguments: %s", args)
    if args.percent > 50:
        logger.warning("a %s%% tip is unusually high", args.percent)
    try:
        tip, total, share = split_bill(args.bill, args.percent,
                                       args.people)
    except ValueError as err:
        print(f"tip: error: {err}", file=sys.stderr)
        return 1
    print(f"Tip ${tip:.2f}, total ${total:.2f}, "
          f"each pays ${share:.2f}")
    return 0
