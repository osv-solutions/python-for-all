import pytest

from prices import parse_price


def test_plain_number():
    assert parse_price("4.50") == 4.5


def test_dollar_sign_and_spaces():
    assert parse_price(" $12 ") == 12.0


def test_thousands_separator():
    assert parse_price("$1,250.00") == 1250.0


def test_not_a_price():
    with pytest.raises(ValueError):
        parse_price("free")
