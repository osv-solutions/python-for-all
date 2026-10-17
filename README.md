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
| `examples/` | Multi-file code that the book builds step by step: the tested code of Chapter 17, the practice web servers of Chapter 19 and Projects 12–13, the packages of Chapter 22, the Tkinter windows and unit converter of Chapter 23, the contact book of Project 14 and the price watcher of Project 15 (each folder has its own README) |
| `requirements.txt` | The packages used from Chapter 16 on, at the versions the book was tested with |

Each folder holds the same code twice: as a plain Python script (`.py`) and as a
Jupyter notebook (`.ipynb`) with the book's section headings.

## Getting started

You need Python 3.14 or newer (Chapter 1 shows how to install it). Until
Chapter 16, the code uses only Python and its standard library, so there is
nothing else to install. For the later chapters, create a virtual environment
and install the packages (Chapter 16 explains each step):

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

Run a chapter's code from its folder:

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
and reports any that fail. If `pytest` is installed, it also runs the tests in
`examples/`:

```bash
python run_all.py
```

## The Python for… series

*Python for All* is Book 1 of the *Python for…* series. Each book takes one
field and builds on this one, with the same layout, fully tested code and
complete projects. On Amazon, search for "Python for… series" to see every
book released so far. Titles and order of the planned books may change.

| # | Title | Status |
|---|---|---|
| 1 | Python for All | This book |
| 2 | Python for Data Science | Coming soon |
| 3 | Python for Machine Learning | Coming soon |
| 4 | Python for Deep Learning | Coming soon |
| 5 | Python for Office Automation | Planned |
| 6 | Python for Generative AI and Agentic AI | Planned |
| 7 | Python for Data Engineering | Planned |
| 8 | Python for DevOps and Automation | Planned |
| 9 | Python for Network Automation | Planned |
| 10 | Python for Testing and QA | Planned |
| 11 | Python for Cloud (AWS) | Planned |
| 12 | Python for MLOps | Planned |
| 13 | Python for NLP | Planned |
| 14 | Python for Computer Vision | Planned |
| 15 | Python for IoT: Raspberry Pi, Arduino and ESP32 | Planned |
| 16 | Python for Robotics | Planned |
| 17 | Python for Web Development | Planned |
| 18 | Python for Desktop Applications (Tkinter and PySide6) | Planned |
| 19 | Clean Python: Best Practices and Design Patterns | Planned |
| 20 | Python for Cyber Security and Ethical Hacking | Planned |
| 21 | Python for Healthcare Data | Planned |
| 22 | Python for Finance and Trading | Planned |
| 23 | Python for Kids | Planned |
| 24 | Python for Game Development | Planned |
| 25 | Python Interview Prep | Planned |

## License

The code is provided for learning. You may use and adapt it in your own
programs, including commercial ones, without asking permission. Attribution is
appreciated but not required.
