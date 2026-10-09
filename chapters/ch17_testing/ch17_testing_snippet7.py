"""Code from "17.10 Writing the test first" that is shown in the book but not run on its own:
it needs your own data, a server or extra setup, or it is one step of an example
that the book builds up gradually. See the book for details."""

from prices import parse_price


def test_plain_number():
    assert parse_price("4.50") == 4.5


def test_dollar_sign_and_spaces():
    assert parse_price(" $12 ") == 12.0
