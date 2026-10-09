"""Split a restaurant bill, tip included."""


def split_bill(bill, tip_percent, people):
    """Return the tip, the total and each person's share."""
    if people < 1:
        raise ValueError("people must be at least 1")
    tip = bill * tip_percent / 100
    total = bill + tip
    return tip, total, total / people
