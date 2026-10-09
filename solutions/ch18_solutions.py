"""Solutions to the Chapter 18 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch18_solutions.py

The explanations are in ch18_solutions.md."""

# %% Exercise 18.1
MIN_PASSWORD_LENGTH = 8

def is_strong_password(password: str) -> bool:
    """Return True if the password is long and not only letters."""
    long_enough = len(password) >= MIN_PASSWORD_LENGTH
    return long_enough and not password.isalpha()

is_strong = is_strong_password("tulip2025")
print(is_strong, is_strong_password("tulips"))

# %% Exercise 18.2
def ticket_price(age: int) -> int:
    """Return the ticket price in dollars for a visitor's age."""
    if age < 0:
        raise ValueError(f"age can't be negative: {age}")
    if age < 5:
        return 0
    if age < 18 or age >= 65:
        return 8
    return 15

# %% Exercise 18.2
def split_bill(bill: float, tip_percent: float,
               people: int) -> tuple[float, float, float]:
    """Return the tip, the total and each person's share."""
    if people < 1:
        raise ValueError("people must be at least 1")
    tip = bill * tip_percent / 100
    total = bill + tip
    return tip, total, total / people

# %% Exercise 18.2
print(ticket_price.__annotations__)
for name, hint in split_bill.__annotations__.items():
    print(f"{name:12} {hint}")

# %% Exercise 18.4
from dataclasses import dataclass

@dataclass
class Book:
    title: str
    author: str
    year: int
    rating: float | None = None

type Library = list[Book]

def best_rated(books: Library) -> Book | None:
    """Return the book with the highest rating, or None."""
    rated = [book for book in books if book.rating is not None]
    if not rated:
        return None
    return max(rated, key=lambda book: book.rating or 0)

# %% Exercise 18.4
shelf = [
    Book("The Hobbit", "J. R. R. Tolkien", 1937, 4.7),
    Book("Dune", "Frank Herbert", 1965),
    Book("Emma", "Jane Austen", 1815, 4.2),
]
best = best_rated(shelf)
if best is not None:
    print(best.title, best.rating)
print(best_rated([Book("Dune", "Frank Herbert", 1965)]))

# %% Exercise 18.6
def p(o):
    return (sum(o) * 0.9 if sum(o) > 100
            else sum(o) + 5 if sum(o) < 20 else sum(o))

cases = [[], [10], [19.99], [20], [50, 50], [100], [100.01],
         [60, 70], [5, 5, 5]]
expected = [p(case) for case in cases]
print(expected)

# %% Exercise 18.6
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

# %% Exercise 18.6
def order_total(prices: list[float]) -> float:
    """Return what the customer pays for items with these prices."""
    return amount_due(sum(prices))

for case, old in zip(cases, expected):
    assert order_total(case) == old, case
print("all", len(cases), "cases unchanged")
