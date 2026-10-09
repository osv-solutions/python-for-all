import pytest

from cart import Cart


@pytest.fixture
def cart():
    c = Cart(tax_rate=0)
    c.add("pen", 1.50, 4)
    c.add("notebook", 3.25)
    return c


def test_total(cart):
    assert cart.total == 9.25


def test_adding_again_raises_quantity(cart):
    cart.add("pen", 1.50)
    assert cart.total == 10.75


def test_remove(cart):
    cart.remove("notebook")
    assert cart.total == 6.0


def test_remove_missing_item(cart):
    with pytest.raises(KeyError):
        cart.remove("stapler")


def test_save_and_load(cart, tmp_path):
    path = tmp_path / "cart.json"
    cart.save(path)
    copy = Cart(tax_rate=0)
    copy.load(path)
    assert copy.total == cart.total
