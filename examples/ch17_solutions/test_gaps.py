import pytest

from cart import Cart
from tickets import split_bill


def test_cart_rejects_negative_price():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add("pen", -1.50)


def test_split_bill_needs_people():
    with pytest.raises(ValueError, match="at least 1"):
        split_bill(100, 10, 0)
