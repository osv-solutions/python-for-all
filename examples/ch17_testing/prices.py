def parse_price(text):
    """Turn a price such as "$1,250.00" into a number."""
    cleaned = text.strip().removeprefix("$").replace(",", "")
    return float(cleaned)
