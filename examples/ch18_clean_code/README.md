# Chapter 18: the clean-code example

The finished `grades.py` and `summary.py` of Chapter 18, with the `pyproject.toml`
that sets `ruff`'s line length. With `ruff` and `mypy` installed
(`python -m pip install -r requirements.txt` from the top of the repository),
run the checks and the program from this folder:

```bash
cd examples/ch18_clean_code
ruff check
ruff format --check
python -m mypy .
python summary.py
```

`ruff` reports `All checks passed!` and `mypy` finds no issues. The book also shows
earlier versions of these files, with type errors and lint problems, on the way to
this final state.
