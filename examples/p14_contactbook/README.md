# contactbook

A contact book for the command line: Project 14 of
*Python for All*. Install it into a fresh virtual environment, with the
development tools, and try the `contacts` command:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
contacts --file demo.json add "Ada Lovelace" -e ada@example.com
contacts --file demo.json list
```

Without `--file`, the contacts live in `~/.contacts.json`, or in the file
named by the `CONTACTS_FILE` environment variable.

Before each release, run the checks:

```bash
python -m pytest
ruff check
ruff format --check
python -m mypy src
```
