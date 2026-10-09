# Python for All: companion code

The code for **Python for All: A Hands-On Guide from Your First Program to Real
Projects** by Vamsi Krishna Kandala, Book 1 of the *Python for…* series.

Every listing in the book is here exactly as printed, together with worked,
tested solutions to every chapter's exercises.

| Folder | Contents |
|---|---|
| `chapters/` | One folder per chapter, for example `ch03_text/` |
| `projects/` | One folder per project, for example `p01_guessing_game/` |
| `solutions/` | Worked solutions to each chapter's exercises: start with `solutions/README.md` |

Each folder holds the same code twice: as a plain Python script (`.py`) and as a
Jupyter notebook (`.ipynb`) with the book's section headings.

## Getting started

You need Python 3.14 or newer (Chapter 1 shows how to install it). Until
Chapter 16, the code uses only Python and its standard library, so there is
nothing else to install. Run a chapter's code from its folder:

```bash
cd chapters/ch02_values
python ch02_values.py
```

On macOS and Linux, type `python3` instead of `python` if `python` is not found.

## Programs that ask you to type

Many programs ask questions with `input()`. When you run them, type your own
answers. To replay the answers used in the book instead, feed the matching
`.inputs.txt` file to the program:

```bash
python ch05_loops.py < ch05_loops.inputs.txt
```

A few examples in the book stop with an error on purpose, to show how to read
error messages. In the scripts, these examples are wrapped so that the error
is printed and the script carries on.

## Checking everything

`run_all.py` runs every script in the repository, replaying the book's answers,
and reports any that fail:

```bash
python run_all.py
```

## License

The code is provided for learning. You may use and adapt it in your own
programs, including commercial ones, without asking permission. Attribution is
appreciated but not required.
