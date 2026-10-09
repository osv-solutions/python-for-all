# Solutions: Chapter 16, Virtual Environments and Packages

Worked solutions to the exercises at the end of Chapter 16 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch16_solutions.ipynb`](ch16_solutions.ipynb) or the script `ch16_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 16.1

*Create a folder `env_practice`, make a virtual environment in it, activate it, and print `sys.prefix` with and without the environment active.*

On macOS and Linux:

```bash
mkdir env_practice
cd env_practice
python3 -m venv .venv
source .venv/bin/activate
python -c "import sys; print(sys.prefix)"
deactivate
python3 -c "import sys; print(sys.prefix)"
```

On Windows, write `python` instead of `python3`, and activate with `.venv\Scripts\activate`. `python -c` runs the code in quotes without a script file. With the environment active, `sys.prefix` ends in `env_practice/.venv` (on Windows, `env_practice\.venv`): Python is using the environment. After `deactivate`, it shows the folder where Python itself is installed, which differs from computer to computer, for example `/usr` on many Linux systems or `C:\Users\Asha\AppData\Local\Programs\Python\Python314` on Windows. The prompt of the terminal tells you the same thing at a glance: `(.venv)` appears in front of it while the environment is active.

## Exercise 16.2

*Install `tabulate`, then compare the output of `pip list`, `pip show tabulate` and `pip freeze`.*

```bash
python -m pip install tabulate
python -m pip list
python -m pip show tabulate
python -m pip freeze
```

In a fresh environment, `pip list` shows a table with two packages, `pip` and `tabulate`, and their versions. `pip show tabulate` gives the details of one package: version, summary, home page, license, where it is installed, and the lines `Requires:` and `Required-by:`, both empty for `tabulate`, because it needs no other packages and none of the installed ones need it. `pip freeze` prints `tabulate==0.10.0` and nothing else.

The difference between `list` and `freeze` is their purpose. `list` is for people: a readable table of everything installed, including `pip` itself. `freeze` is for files: it writes requirements in the exact `name==version` format that `pip install -r` reads back, and it leaves out the tools that every environment has anyway, such as `pip`.

## Exercise 16.3

*Print the planets table in the `tabulate` styles `grid`, `github` and `simple_outline`.*

```python
from tabulate import tabulate

rows = [["Mercury", 0.39, 88], ["Venus", 0.72, 225],
        ["Earth", 1.00, 365], ["Mars", 1.52, 687]]
headers = ["Planet", "Distance (AU)", "Year (days)"]
for style in ["grid", "github", "simple_outline"]:
    print(style)
    print(tabulate(rows, headers=headers, tablefmt=style))
    print()
```

Output:

```text
grid
+----------+-----------------+---------------+
| Planet   |   Distance (AU) |   Year (days) |
+==========+=================+===============+
| Mercury  |            0.39 |            88 |
+----------+-----------------+---------------+
| Venus    |            0.72 |           225 |
+----------+-----------------+---------------+
| Earth    |            1    |           365 |
+----------+-----------------+---------------+
| Mars     |            1.52 |           687 |
+----------+-----------------+---------------+

github
| Planet   |   Distance (AU) |   Year (days) |
|----------|-----------------|---------------|
| Mercury  |            0.39 |            88 |
| Venus    |            0.72 |           225 |
| Earth    |            1    |           365 |
| Mars     |            1.52 |           687 |

simple_outline
┌──────────┬─────────────────┬───────────────┐
│ Planet   │   Distance (AU) │   Year (days) │
├──────────┼─────────────────┼───────────────┤
│ Mercury  │            0.39 │            88 │
│ Venus    │            0.72 │           225 │
│ Earth    │            1    │           365 │
│ Mars     │            1.52 │           687 │
└──────────┴─────────────────┴───────────────┘
```

`grid` draws a box around every cell with `+`, `-` and `|`, and marks the header with `=`. `github` produces a Markdown table, the format used in README files on GitHub, which turns into a real table when the page is displayed. `simple_outline` draws a neat frame with box-drawing characters. The data and the alignment of the numbers are the same in all three; only the decoration changes. `tabulate` offers more than thirty styles, listed in its documentation.

## Exercise 16.4

*Install `tabulate` 0.9.0, check the version with `pip show`, then upgrade it.*

```bash
python -m pip install "tabulate==0.9.0"
python -m pip show tabulate
python -m pip install -U tabulate
```

If `tabulate` is already installed, the first command replaces it with version 0.9.0. `pip show` then reports `Version: 0.9.0`. Before upgrading, `pip` notes what is installed already, then downloads the new version and replaces the old one:

```output
Requirement already satisfied: tabulate in ./.venv/lib/python3.14/site-packages (0.9.0)
Collecting tabulate
  Downloading tabulate-0.10.0-py3-none-any.whl.metadata (40 kB)
Downloading tabulate-0.10.0-py3-none-any.whl (39 kB)
Installing collected packages: tabulate
  Attempting uninstall: tabulate
    Found existing installation: tabulate 0.9.0
    Uninstalling tabulate-0.9.0:
      Successfully uninstalled tabulate-0.9.0
Successfully installed tabulate-0.10.0
```

The messages show the three stages of an upgrade: `pip` finds the version already installed, uninstalls it, and installs the new one. An environment never holds two versions of the same package. That is why two projects that need different versions each need their own environment.

## Exercise 16.5

*Write a `requirements.txt` by hand for any 0.10 version of `tabulate` and `pytest` version 8 or newer, and install from it in a fresh environment.*

```text
tabulate~=0.10.0
pytest>=8
```

`~=0.10.0` allows 0.10.0 and any later 0.10.x, but not 0.11, which suits the "any 0.10 version" in the task. `>=8` allows version 8 and everything newer, including future major versions. A careful project would write `pytest>=8,<10`, to avoid a future major version that could change things. Then, in a new folder:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pip freeze
```

`pip freeze` now lists `tabulate==0.10.0` and the newest `pytest` (9.1.1 when this book was tested), together with the packages that `pytest` depends on, such as `pluggy` and `iniconfig`. A hand-written requirements file states what the project *needs*; the output of `freeze` records exactly what was *installed*. Many projects keep both.

## Exercise 16.6

*Look up `requests` on pypi.org: its latest version, license, release date and documentation. Is it trustworthy?*

Package details change over time, so check them yourself. In October 2026, the page `pypi.org/project/requests` showed:

- **Latest version:** 2.34.2, released on May 14, 2026.

- **License:** Apache-2.0, a permissive license that allows use in almost any project.

- **Documentation:** `requests.readthedocs.io`, with the source code at `github.com/psf/requests`.

It passes every check of the chapter. It is maintained, with regular releases over more than a decade. It is one of the most downloaded packages on PyPI, so millions of programs rely on it and bugs are found quickly. Its documentation is thorough, its license is permissive, and its repository belongs to the Python Software Foundation's GitHub organization (`psf`). Chapter 19 uses it to talk to web services.

## Exercise 16.7

*Rewrite the monthly report of Project 5 with `tabulate`.*

This solution recreates the sample expenses of Project 5 and the `totals` function from its Step 4 (not printed here), then builds the report as a list of rows:

<details>
<summary>Setup code: recreates the data and helpers from the chapter (click to show)</summary>

```python
import csv
from datetime import date
from pathlib import Path

CATEGORIES = ["food", "transport", "housing", "fun", "other"]
Path("expenses.csv").write_text("""date,category,description,amount
2026-09-01,housing,September rent,1200.00
2026-09-03,food,Groceries,86.40
2026-09-09,transport,Bus pass,55.00
2026-09-14,fun,Concert tickets,90.00
2026-09-20,food,Groceries,74.25
2026-09-25,food,Dinner out,48.10
2026-10-01,housing,October rent,1200.00
2026-10-02,food,Groceries,92.30
2026-10-06,fun,Cinema,24.00
""", encoding="utf-8")
```

</details>

<details>
<summary>Setup code: recreates the data and helpers from the chapter (click to show)</summary>

```python
with open("expenses.csv", newline="", encoding="utf-8") as f:
    expenses = [{"date": date.fromisoformat(r["date"]),
                 "category": r["category"],
                 "amount": float(r["amount"])}
                for r in csv.DictReader(f)]

def totals(expenses):
    """Return {(month, category): total}, with months as "YYYY-MM"."""
    result = {}
    for e in expenses:
        key = (e["date"].strftime("%Y-%m"), e["category"])
        result[key] = result.get(key, 0) + e["amount"]
    return result
```

</details>

```python
from tabulate import tabulate

def report(expenses):
    table = totals(expenses)
    months = sorted({month for month, cat in table})
    rows = [[cat] + [table.get((m, cat), 0) for m in months]
            for cat in CATEGORIES]
    month_totals = [sum(table.get((m, c), 0) for c in CATEGORIES)
                    for m in months]
    rows.append(["total"] + month_totals)
    print(tabulate(rows, headers=[""] + months, floatfmt=".2f"))

report(expenses)
```

Output:

```text
             2026-09    2026-10
---------  ---------  ---------
food          208.75      92.30
transport      55.00       0.00
housing      1200.00    1200.00
fun            90.00      24.00
other           0.00       0.00
total        1553.75    1316.30
```

The function now only *collects* the numbers: one row per category, with the category's name followed by its total for each month, and a final row of monthly totals. `tabulate` does all the formatting: it sizes the columns, right-aligns the numbers, and `floatfmt=".2f"` shows every amount with two decimals, replacing the many f-strings with widths of the original. The rule under the headers comes free. A whole number of 0 for a month without spending also prints as `0.00`, because `floatfmt` applies to every number in a column of floats.
