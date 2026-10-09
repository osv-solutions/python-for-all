"""Code from "17.3 Your first tests with pytest" that is shown in the book but not run on its own:
it needs your own data, a server or extra setup, or it is one step of an example
that the book builds up gradually. See the book for details."""

from tickets import ticket_price


def test_adult_pays_full_price():
    assert ticket_price(30) == 15


def test_child_pays_reduced_price():
    assert ticket_price(10) == 8


def test_senior_pays_reduced_price():
    assert ticket_price(70) == 8
