import pytest

from tickets import split_bill, ticket_price


def test_adult_pays_full_price():
    assert ticket_price(30) == 15


def test_child_pays_reduced_price():
    assert ticket_price(10) == 8


def test_senior_pays_reduced_price():
    assert ticket_price(70) == 8


def test_exactly_65_is_senior():
    assert ticket_price(65) == 8


def test_negative_age_is_rejected():
    with pytest.raises(ValueError):
        ticket_price(-1)


def test_error_message_shows_the_age():
    with pytest.raises(ValueError, match="negative: -3"):
        ticket_price(-3)


def test_split_bill():
    tip, total, share = split_bill(48.5, 20, 3)
    assert tip == pytest.approx(9.7)
    assert total == pytest.approx(58.2)
    assert share == pytest.approx(19.4)


@pytest.mark.parametrize("age, price", [
    (0, 0), (4, 0), (5, 8), (17, 8),
    (18, 15), (64, 15), (65, 8), (66, 8),
])
def test_price_at_boundaries(age, price):
    assert ticket_price(age) == price
