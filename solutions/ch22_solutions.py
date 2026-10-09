"""Solutions to the Chapter 22 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch22_solutions.py

The explanations are in ch22_solutions.md."""

# %% Exercise 22.1
import sys

def main(argv):
    if not argv:
        print("usage: shout.py WORD...", file=sys.stderr)
        return 2
    print(" ".join(argv).upper())
    return 0

print("exit code", main(["hello", "there"]))
print("exit code", main([]))

# %% Exercise 22.2
import argparse

parser = argparse.ArgumentParser(
    prog="tip", description="Split a bill, tip included.")
parser.add_argument("bill", type=float, help="the bill in dollars")
parser.add_argument("--version", action="version",
                    version="%(prog)s 1.0.0")
try:
    parser.parse_args(["--version"])
except SystemExit as exc:
    print("exit code", exc.code)

# %% Exercise 22.3
def c_to_f(celsius):
    return celsius * 9 / 5 + 32

def f_to_c(fahrenheit):
    return (fahrenheit - 32) * 5 / 9

convert = argparse.ArgumentParser(
    prog="convert", description="Convert a temperature.")
convert.add_argument("degrees", type=float,
                     help="the temperature to convert")
convert.add_argument("--to", required=True, choices=["c", "f"],
                     help="the unit to convert to")
convert.add_argument("--decimals", type=int, default=1,
                     help="decimal places (default: %(default)s)")

# %% Exercise 22.3
def main(argv):
    args = convert.parse_args(argv)
    if args.to == "f":
        result = c_to_f(args.degrees)
    else:
        result = f_to_c(args.degrees)
    print(f"{result:.{args.decimals}f} °{args.to.upper()}")

main(["100", "--to", "f"])
main(["98.6", "--to", "c", "--decimals", "2"])
try:
    main(["20", "--to", "k"])
except SystemExit as exc:
    print("exit code", exc.code)

# %% Exercise 22.4
todo = argparse.ArgumentParser(prog="todo",
                               description="A tiny to-do list.")
commands = todo.add_subparsers(dest="command", required=True)
add = commands.add_parser("add", help="add a task")
add.add_argument("title", help="what to do")
add.add_argument("--priority", choices=["low", "normal", "high"],
                 default="normal")
show = commands.add_parser("list", help="show the tasks")
show.add_argument("--all", action="store_true",
                  help="include the tasks that are done")
finish = commands.add_parser("done", help="mark a task as done")
finish.add_argument("number", type=int, help="the task's number")
remove = commands.add_parser("remove", help="delete a task")
remove.add_argument("number", type=int, help="the task's number")
print(todo.format_help())

# %% Exercise 22.4
tasks = []

def run(argv):
    args = todo.parse_args(argv)
    if args.command == "add":
        tasks.append([args.title, args.priority, False])
    elif args.command == "list":
        for number, (title, priority, done) in enumerate(tasks, 1):
            if done and not args.all:
                continue
            mark = "x" if done else " "
            print(f"{number}. [{mark}] {title} ({priority})")
    elif args.command == "done":
        tasks[args.number - 1][2] = True
    elif args.command == "remove":
        del tasks[args.number - 1]

# %% Exercise 22.4
for argv in (["add", "Buy milk", "--priority", "high"],
             ["add", "Water the plants"], ["add", "Call Grace"],
             ["done", "1"], ["remove", "2"]):
    run(argv)
run(["list"])
print("---")
run(["list", "--all"])

# %% Exercise 22.5
import logging

logger = logging.getLogger("average")

def read_numbers(lines):
    numbers = []
    for line in lines:
        try:
            number = float(line)
        except ValueError:
            logger.warning("skipping %r", line.strip())
            continue
        logger.debug("read %s", number)
        numbers.append(number)
    return numbers

# %% Exercise 22.5
def average_file(path):
    try:
        with open(path) as f:
            numbers = read_numbers(f)
    except OSError:
        logger.exception("could not read %s", path)
        return None
    return sum(numbers) / len(numbers) if numbers else None

# %% Exercise 22.5
logging.basicConfig(filename="average.log", filemode="w",
                    level=logging.DEBUG, force=True,
                    format="%(levelname)s:%(name)s: %(message)s")
with open("scores.txt", "w") as f:
    f.write("12\n15.5\nabsent\n\n9\n")
print(average_file("scores.txt"))
print(average_file("missing.txt"))
with open("average.log") as f:
    print(f.read())
