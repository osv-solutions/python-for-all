"""Code from "17.8 Many cases with parametrize" that is shown in the book but not run on its own:
it needs your own data, a server or extra setup, or it is one step of an example
that the book builds up gradually. See the book for details."""

@pytest.mark.parametrize("age, price", [
    (0, 0), (4, 0), (5, 8), (17, 8),
    (18, 15), (64, 15), (65, 8), (66, 8),
])
def test_price_at_boundaries(age, price):
    assert ticket_price(age) == price
