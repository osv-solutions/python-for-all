"""Chapter 22: Command-Line Tools and Packaging

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch22_cli_packaging.py

or open the notebook and run the cells in order.
"""

# %% 22.2 Parsing arguments with argparse
import argparse

parser = argparse.ArgumentParser(
    prog="tip", description="Split a bill, tip included.")
parser.add_argument("bill", type=float,
                    help="the bill in dollars")
args = parser.parse_args(["48.50"])
print(args)
print(args.bill + 1)

# %% 22.2 Parsing arguments with argparse
parser.add_argument("-p", "--percent", type=float, default=15,
                    help="tip percentage (default: %(default)s)")
parser.add_argument("-n", "--people", type=int, default=1,
                    help="people sharing (default: %(default)s)")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="explain what the program is doing")
print(parser.parse_args(["48.50"]))
print(parser.parse_args(["48.50", "--percent", "20", "-n", "3"]))
print(parser.parse_args(["-v", "--people=3", "48.50"]))

# %% 22.2 Parsing arguments with argparse
print(parser.format_help())

# %% 22.2 Parsing arguments with argparse
try:
    parser.parse_args(["48.50", "--people", "three"])
except SystemExit as exc:
    print("argparse stopped with exit code", exc.code)

# %% 22.4 Subcommands
todo = argparse.ArgumentParser(prog="todo",
                               description="A tiny to-do list.")
commands = todo.add_subparsers(dest="command", required=True)
add = commands.add_parser("add", help="add a task")
add.add_argument("title", help="what to do")
add.add_argument("--priority", choices=["low", "normal", "high"],
                 default="normal")
commands.add_parser("list", help="show the tasks")
finish = commands.add_parser("done", help="mark a task as done")
finish.add_argument("number", type=int, help="the task's number")
print(todo.parse_args(["add", "Buy milk", "--priority", "high"]))
print(todo.parse_args(["done", "2"]))
print(todo.parse_args(["list"]))

# %% 22.5 Logging instead of print
import logging
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format="%(levelname)s: %(message)s")
logging.debug("details only a developer needs")
logging.info("starting the backup")
logging.warning("the disk is 91% full")
logging.error("could not copy notes.txt")
logging.critical("the backup drive is gone")

# %% 22.5 Logging instead of print
def setup_logging(verbose=False):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.WARNING,
        format="%(levelname)s:%(name)s: %(message)s",
        stream=sys.stdout, force=True)

setup_logging()
logger = logging.getLogger(__name__)
logger.info("not shown: below WARNING")
logger.warning("a %s%% tip is unusually high", 60)

# %% 22.5 Logging instead of print
to_file = logging.FileHandler("tip.log", mode="w")
to_screen = logging.StreamHandler(sys.stdout)
to_screen.setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG, force=True,
                    handlers=[to_file, to_screen],
                    format="%(levelname)s:%(name)s: %(message)s")
logger.debug("bill is %s", 48.5)
logger.warning("people not given, assuming 1")
print("--- tip.log ---")
with open("tip.log") as f:
    print(f.read())

# %% 22.5 Logging instead of print
setup_logging()

def parse_bill(text):
    try:
        return float(text.removeprefix("$"))
    except ValueError:
        logger.exception("not a valid bill: %r", text)
        return None

print(parse_bill("$48.50"))
print(parse_bill("forty"))
