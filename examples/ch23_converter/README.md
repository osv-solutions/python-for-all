# Chapter 23: the unit converter

The mini project of Chapter 23 of *Python for All*: a Tkinter window that
converts lengths, weights and temperatures as you type.

| File | What it holds |
|---|---|
| `conversions.py` | The conversions, with no `tkinter`: `convert`, `parse_number`, `format_result`, `units` |
| `app.py` | The window: `ConverterApp`, a `ttk.Frame` subclass, and `main` |
| `tests/` | `pytest` tests of the conversions and of the window |

```bash
python app.py              # open the converter
python -m pytest           # run the 14 tests
```

The window tests create a hidden window; on a computer without a screen
they are skipped.
