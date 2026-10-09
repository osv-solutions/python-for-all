# Chapter 17: the testing example

The finished code and tests of Chapter 17. With `pytest` installed
(`python -m pip install -r requirements.txt` from the top of the repository),
run the tests from this folder:

```bash
cd examples/ch17_testing
python -m pytest -v
python -m pytest --cov --cov-report=term-missing
```

All 24 tests pass. The book also shows earlier versions of these files, with a
deliberate bug and failing tests, on the way to this final state.
