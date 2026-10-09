# tipcalc

Split a restaurant bill, tip included: the example project of Chapter 22
of *Python for All*. Install it into a fresh virtual environment and try
the `tip` command:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -e .
tip 48.50 --percent 20 --people 3
```

Run the tests with `python -m pytest` (they also run without installing
the package, thanks to the `pythonpath` setting in `pyproject.toml`).
