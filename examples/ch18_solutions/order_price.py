"""Exercise 18.6: the order price, refactored."""

DISCOUNT_FROM = 100
DISCOUNT_RATE = 0.10
SMALL_ORDER_BELOW = 20
SMALL_ORDER_FEE = 5


def amount_due(subtotal: float) -> float:
    """Apply the discount for large orders and the small-order fee."""
    if subtotal > DISCOUNT_FROM:
        return subtotal * (1 - DISCOUNT_RATE)
    if subtotal < SMALL_ORDER_BELOW:
        return subtotal + SMALL_ORDER_FEE
    return subtotal


def order_total(prices: list[float]) -> float:
    """Return what the customer pays for items with these prices."""
    return amount_due(sum(prices))
