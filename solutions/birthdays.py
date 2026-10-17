"""Birthday helpers."""
from datetime import date


def next_birthday(birth, today):
    """Return (date of next birthday, days until it)."""
    year = today.year
    while True:
        try:
            candidate = birth.replace(year=year)
        except ValueError:
            candidate = date(year, 3, 1)
        if candidate >= today:
            return candidate, (candidate - today).days
        year += 1


if __name__ == "__main__":
    print(next_birthday(date(2000, 1, 1), date(2026, 10, 8)))
