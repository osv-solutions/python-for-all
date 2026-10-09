# wordcount

The worked solution to Exercise 22.6 of *Python for All*: a word counter
packaged with `pyproject.toml`, the src layout and tests. Try it in a fresh
virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -e .
wordcount --lines tyger.txt fox.txt
python -m pytest
```
