# Solutions: Chapter 22, Command-Line Tools and Packaging

Worked solutions to the exercises at the end of Chapter 22 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch22_solutions.ipynb`](ch22_solutions.ipynb) or the script `ch22_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 22.1

*Write `shout.py`, which prints its arguments in capitals, or a usage line on standard error and exit code 2 when there are none.*

```python
import sys


def main(argv):
    if not argv:
        print("usage: shout.py WORD...", file=sys.stderr)
        return 2
    print(" ".join(argv).upper())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

```bash
python shout.py hello there
echo $?
python shout.py
echo $?
```

```output
HELLO THERE
0
usage: shout.py WORD...
2
```

`sys.argv[1:]` leaves out the program's own name, so `main` receives only the words. An empty list is false, which makes `if not argv` the test for "no arguments". `main` returns the exit code instead of calling `sys.exit` itself, so it can be tried without a terminal:

```python
import sys

def main(argv):
    if not argv:
        print("usage: shout.py WORD...", file=sys.stderr)
        return 2
    print(" ".join(argv).upper())
    return 0

print("exit code", main(["hello", "there"]))
print("exit code", main([]))
```

Output:

```text
HELLO THERE
exit code 0
exit code 2
```

The second call prints its usage line to standard error, which this page doesn't capture, so only the two exit codes and the shouted words appear. In the terminal, `echo $?` shows the same codes, 0 and 2. (In PowerShell, use `$LASTEXITCODE`.)

## Exercise 22.2

*Add `--version` to the tip parser. What does `parse_args(["--version"])` print, and with which exit code does it stop?*

```python
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
```

Output:

```text
tip 1.0.0
exit code 0
```

`action="version"` works like `-h`: it prints a message on standard output and ends the program at once, with exit code 0, because asking for the version is not an error. `%(prog)s` is replaced by the program's name. That is also why the required `bill` wasn't missed: the program stopped before `argparse` checked for it. `tip --version` in a terminal prints `tip 1.0.0`.

## Exercise 22.3

*Write a parser for `convert 100 --to f`, with the choices `c` and `f` and a `--decimals` option.*

```python
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
```

The two functions are the ones from Chapter 9's `temperature.py`; in a real project you would import them. `required=True` makes `--to` compulsory, which is allowed for options, although most options are optional. The program itself:

```python
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
```

Output:

```text
212.0 °F
37.00 °C
exit code 2
```

100 °C is 212.0 °F, and 98.6 °F is 37.00 °C. The format `.{args.decimals}f` puts the number of decimals into the format specification itself: an f-string can contain a field inside the format part. The unit `k` is not one of the choices, so `argparse` stops with exit code 2; in a terminal it prints `convert: error: argument --to: invalid choice: 'k' (choose from 'c', 'f')` after the usage line.

## Exercise 22.4

*Extend the to-do tool with `remove NUMBER` and a `--all` flag for `list`.*

```python
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
```

Output:

```text
usage: todo [-h] {add,list,done,remove} ...

A tiny to-do list.

positional arguments:
  {add,list,done,remove}
    add                 add a task
    list                show the tasks
    done                mark a task as done
    remove              delete a task

options:
  -h, --help            show this help message and exit
```

`list` now has a parser of its own with a flag, and `remove` takes a number like `done`. The help lists all four subcommands. Then the program:

```python
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
```

```python
for argv in (["add", "Buy milk", "--priority", "high"],
             ["add", "Water the plants"], ["add", "Call Grace"],
             ["done", "1"], ["remove", "2"]):
    run(argv)
run(["list"])
print("---")
run(["list", "--all"])
```

Output:

```text
2. [ ] Call Grace (normal)
---
1. [x] Buy milk (high)
2. [ ] Call Grace (normal)
```

Three tasks are added, the first is marked as done and the second, "Water the plants", is removed. Plain `list` skips the finished task and shows only "Call Grace", which is now number 2. `list --all` shows both. The numbers come from `enumerate` over the whole list, so a task keeps the same number whether or not finished tasks are shown, and `done 2` always means the task shown as 2.

## Exercise 22.5

*Write `average_file(path)` that logs each number, warns about lines that aren't numbers, and logs a missing file with `logger.exception`.*

The reading of the lines goes into a helper, which keeps both functions short:

```python
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
```

`float` accepts the spaces and the newline around a number, so `float("15.5\n")` is 15.5 and the lines need no stripping. In a module `average.py`, `logging.getLogger(__name__)` would give the logger the same name, `average`. The function that opens the file:

```python
def average_file(path):
    try:
        with open(path) as f:
            numbers = read_numbers(f)
    except OSError:
        logger.exception("could not read %s", path)
        return None
    return sum(numbers) / len(numbers) if numbers else None
```

Looping over an open file gives its lines, so `read_numbers(f)` works directly on the file. A file without a single number returns `None` rather than dividing by zero. Now send the log to a file, try both cases and look at the log:

```python
logging.basicConfig(filename="average.log", filemode="w",
                    level=logging.DEBUG, force=True,
                    format="%(levelname)s:%(name)s: %(message)s")
with open("scores.txt", "w") as f:
    f.write("12\n15.5\nabsent\n\n9\n")
print(average_file("scores.txt"))
print(average_file("missing.txt"))
with open("average.log") as f:
    print(f.read())
```

Output:

```text
12.166666666666666
None
DEBUG:average: read 12.0
DEBUG:average: read 15.5
WARNING:average: skipping 'absent'
WARNING:average: skipping ''
DEBUG:average: read 9.0
ERROR:average: could not read missing.txt
Traceback (most recent call last):
  File "average.py", line 3, in average_file
    with open(path) as f:
         ~~~~^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'missing.txt'
```

Only the two results reach the screen: 12.166666666666666, the average of 12, 15.5 and 9, and `None` for the missing file. Everything else is in `average.log`: a `DEBUG` line for each number, a `WARNING` for the word `absent` and another for the empty line, and an `ERROR` for the missing file followed by its traceback, which points to the `open` line. `filemode="w"` starts a fresh log on every run.

## Exercise 22.6

*Package a word counter as a project `wordcount` with the src layout, a command, tests and a wheel.*

The project is in `examples/ch22_wordcount/` in the companion repository:

```text
wordcount/
├── pyproject.toml
├── README.md
├── fox.txt, tyger.txt      two files to count
├── src/
│   └── wordcount/
│       ├── __init__.py
│       ├── __main__.py
│       └── cli.py
└── tests/
    └── test_wordcount.py
```

`pyproject.toml` follows the `tipcalc` example of the chapter, with a new name, version, description and command:

```toml
[project]
name = "wordcount"
version = "0.1.0"
description = "Count the words and lines in text files."
requires-python = ">=3.10"
license = "MIT"
authors = [{ name = "Ada Lovelace" }]
dependencies = []

[project.scripts]
wordcount = "wordcount.cli:main"
```

The `[build-system]` and `[tool.pytest.ini_options]` tables are the same as in `tipcalc`. The counting functions go in `__init__.py`:

```python
"""Count the words and lines in text."""


def count_words(text):
    """Return the number of words in text."""
    return len(text.split())


def count_lines(text):
    """Return the number of lines in text."""
    return len(text.splitlines())
```

`split()` without an argument splits at any run of spaces, tabs and newlines and ignores them at the ends, so it counts words correctly even with double spaces. In `cli.py`, the parser takes one or more files:

```python
def build_parser():
    parser = argparse.ArgumentParser(
        prog="wordcount", description="Count the words in files.")
    parser.add_argument("files", nargs="+", help="the files to count")
    parser.add_argument("--lines", action="store_true",
                        help="count lines as well")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="explain what the program is doing")
    return parser
```

`nargs="+"` collects one or more arguments into a list, so `args.files` is a list of names. A function `report(name, text, lines)`, also in `cli.py`, formats one line of the report, and `setup_logging(verbose)` holds the `basicConfig` call of the chapter. Then `main`:

```python
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
```

A file that can't be read doesn't stop the others: the error goes to standard error, the loop carries on, and the exit code at the end is 1 if any file failed. `err.strerror` is the operating system's short description of the problem. The tests use `tmp_path` and `capsys` together:

```python
def test_main_counts_a_file(tmp_path, capsys):
    path = tmp_path / "poem.txt"
    path.write_text("Tyger Tyger, burning bright,\nIn the forests\n")
    assert main([str(path), "--lines"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("     2 lines     7 words")
```

The file also tests `count_words`, `count_lines` and a missing file. Install the project in a fresh environment and try the command:

```bash
cd wordcount
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -e .
wordcount tyger.txt fox.txt
wordcount --lines tyger.txt fox.txt
wordcount -v fox.txt missing.txt
echo $?
```

```output
    20 words  tyger.txt
     9 words  fox.txt
     4 lines    20 words  tyger.txt
     2 lines     9 words  fox.txt
DEBUG:wordcount.cli: reading fox.txt
     9 words  fox.txt
DEBUG:wordcount.cli: reading missing.txt
wordcount: missing.txt: No such file or directory
1
```

With `-v`, a `DEBUG` line announces each file; the missing file is reported and the exit code is 1, while `fox.txt` was still counted. `wordcount` on its own stops with `the following arguments are required: files` and exit code 2. Finally, with `pytest` and `build` installed in the environment, run the tests and build the package:

```bash
python -m pytest -q
python -m build
```

```output
....                                                                 [100%]
4 passed in 0.02s
...
Successfully built wordcount-0.1.0.tar.gz and wordcount-0.1.0-py3-none-any.whl
```

The four tests pass, and `dist/` holds the wheel and the sdist (the build output is shortened). To publish this project you would need another name: `wordcount` is already taken on PyPI, so something like `ada-wordcount` would do, with the command name in `[project.scripts]` unchanged.
