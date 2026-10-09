"""Code from "17.4 When a test fails" that is shown in the book but not run on its own:
it needs your own data, a server or extra setup, or it is one step of an example
that the book builds up gradually. See the book for details."""

def test_exactly_65_is_senior():
    assert ticket_price(65) == 8
