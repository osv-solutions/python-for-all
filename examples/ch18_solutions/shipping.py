"""Exercise 18.5: shipping costs, after ruff and by-hand fixes."""

PRICE_PER_KG = 2.5
EXPRESS_FEE = 10


def shipping_cost(weight_kg: float, express: bool = False) -> float:
    """Return the shipping cost of a parcel in dollars."""
    cost = weight_kg * PRICE_PER_KG
    if express:
        cost += EXPRESS_FEE
    return cost
