"""Ticket prices and bill splitting, from Chapters 4 and 8."""


def ticket_price(age):
    """Return the ticket price in dollars for a visitor's age."""
    if age < 0:
        raise ValueError(f"age can't be negative: {age}")
    if age < 5:
        return 0
    if age < 18 or age >= 65:
        return 8
    return 15


def split_bill(bill, tip_percent, people):
    """Return the tip, the total and each person's share."""
    if people < 1:
        raise ValueError("people must be at least 1")
    tip = bill * tip_percent / 100
    total = bill + tip
    return tip, total, total / people
