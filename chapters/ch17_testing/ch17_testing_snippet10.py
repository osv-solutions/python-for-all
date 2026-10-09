"""Code from "17.10 Writing the test first" that is shown in the book but not run on its own:
it needs your own data, a server or extra setup, or it is one step of an example
that the book builds up gradually. See the book for details."""

def test_thousands_separator():
    assert parse_price("$1,250.00") == 1250.0
