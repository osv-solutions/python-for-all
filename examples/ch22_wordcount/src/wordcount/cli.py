"""The command line: wordcount FILE... [--lines] [-v]."""
import argparse
import logging
import sys

from wordcount import count_lines, count_words

logger = logging.getLogger(__name__)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="wordcount", description="Count the words in files.")
    parser.add_argument("files", nargs="+", help="the files to count")
    parser.add_argument("--lines", action="store_true",
                        help="count lines as well")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="explain what the program is doing")
    return parser


def report(name, text, lines):
    """Return one line of the report for a file."""
    result = f"{count_words(text):6} words  {name}"
    if lines:
        result = f"{count_lines(text):6} lines" + result
    return result


def setup_logging(verbose):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.WARNING,
        format="%(levelname)s:%(name)s: %(message)s")


def main(argv=None):
    args = build_parser().parse_args(argv)
    setup_logging(args.verbose)
    status = 0
    for name in args.files:
        logger.debug("reading %s", name)
        try:
            with open(name, encoding="utf-8") as f:
                text = f.read()
        except OSError as err:
            print(f"wordcount: {name}: {err.strerror}",
                  file=sys.stderr)
            status = 1
        else:
            print(report(name, text, args.lines))
    return status
