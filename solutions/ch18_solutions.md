# Solutions: Chapter 18, Type Hints and Clean Code

Worked solutions to the exercises at the end of Chapter 18 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch18_solutions.ipynb`](ch18_solutions.ipynb) or the script `ch18_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

The files for Exercises 18.3, 18.5 and 18.6 are in `examples/ch18_solutions/` in the companion repository, together with a `pyproject.toml` for `ruff`. From that folder, with `ruff` and `mypy` installed, `ruff check` reports `All checks passed!` and `python -m mypy .` reports `Success: no issues found in 3 source files`.

## Exercise 18.1

*Rewrite `chk` with good names, a constant and a boolean named as a question.*

```python
MIN_PASSWORD_LENGTH = 8

def is_strong_password(password: str) -> bool:
    """Return True if the password is long and not only letters."""
    long_enough = len(password) >= MIN_PASSWORD_LENGTH
    return long_enough and not password.isalpha()

is_strong = is_strong_password("tulip2025")
print(is_strong, is_strong_password("tulips"))
```

Output:

```text
True False
```

`chk` said nothing; `is_strong_password` says what is checked and, starting with `is_`, that the answer is yes or no. The magic number 8 is now `MIN_PASSWORD_LENGTH`, so the rule can be changed in one place, and the intermediate name `long_enough` splits the condition into two readable halves. `"tulip2025"` has 9 characters and contains digits, so it is strong: `True`. `"tulips"` is too short and only letters: `False`. The result variable `ok` became `is_strong`, which reads well in a later `if is_strong:`.

## Exercise 18.2

*Add type hints to `ticket_price` and `split_bill` from Chapter 17, then print their `__annotations__`.*

```python
def ticket_price(age: int) -> int:
    """Return the ticket price in dollars for a visitor's age."""
    if age < 0:
        raise ValueError(f"age can't be negative: {age}")
    if age < 5:
        return 0
    if age < 18 or age >= 65:
        return 8
    return 15
```

```python
def split_bill(bill: float, tip_percent: float,
               people: int) -> tuple[float, float, float]:
    """Return the tip, the total and each person's share."""
    if people < 1:
        raise ValueError("people must be at least 1")
    tip = bill * tip_percent / 100
    total = bill + tip
    return tip, total, total / people
```

Ages and prices are whole numbers, so `ticket_price` takes and returns an `int`. Money can have cents, so `bill` and `tip_percent` are floats (an `int` is accepted too), while `people` must be a whole number. The return type `tuple[float, float, float]` says that exactly three floats come back. Printing the hints:

```python
print(ticket_price.__annotations__)
for name, hint in split_bill.__annotations__.items():
    print(f"{name:12} {hint}")
```

Output:

```text
{'age': <class 'int'>, 'return': <class 'int'>}
bill         <class 'float'>
tip_percent  <class 'float'>
people       <class 'int'>
return       tuple[float, float, float]
```

A simple class prints as `<class 'int'>`, and a generic type such as `tuple[float, float, float]` prints the way it was written. The parameters come in order, followed by `return`. Nothing else changed: the hints don't affect how the functions run.

## Exercise 18.3

*Write `lowest_score`, use its result without checking for `None`, read the `mypy` error, and fix the call.*

The first version ends with a careless call:

```python
"""Exercise 18.3: a student's lowest score."""

type Scores = dict[str, list[int]]


def lowest_score(scores: Scores, name: str) -> int | None:
    """Return the student's lowest score, or None if unknown."""
    if name not in scores:
        return None
    return min(scores[name])


scores = {"Ada": [92, 88], "Grace": [75, 81]}
print(lowest_score(scores, "Ada") * 2)
```

It runs and prints 176, because Ada is known. `mypy` sees what could happen with another name:

```bash
python -m mypy lowest.py
```

```output
lowest.py:14: error: Unsupported operand types for * ("None" and "int")  [operator]
lowest.py:14: note: Left operand is of type "int | None"
Found 1 error in 1 file (checked 1 source file)
```

The error says that the left side of `*` could be `None`, and the note gives the full type, `int | None`, straight from the hint. For an unknown student such as Alan, the program would stop with `TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'`. The fix stores the result and checks it:

```python
scores = {"Ada": [92, 88], "Grace": [75, 81]}
lowest = lowest_score(scores, "Ada")
if lowest is not None:
    print(lowest * 2)
```

Inside the `if`, `mypy` narrows the type to `int`, and `python -m mypy lowest.py` reports `Success: no issues found in 1 source file`. The program still prints 176. A real program would also say something in an `else` branch, such as "unknown student". The `type Scores` alias keeps the function's first line short.

## Exercise 18.4

*Write a data class `Book` with an optional rating, a type alias `Library`, and `best_rated`.*

```python
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
```

`rating: float | None = None` makes the rating optional: a book without one gets `None`. `best_rated` first keeps only rated books, so that `max` never compares `None` with a number, and returns `None` if no book is rated, which its hint announces. The `key` says `book.rating or 0` instead of just `book.rating`: every rating in `rated` is a float, but a type checker doesn't follow the list comprehension's filter, and `or 0` gives it a function that always returns a number. Without it, `mypy` reports that the `key` function may return `None`, which can't be compared.

```python
shelf = [
    Book("The Hobbit", "J. R. R. Tolkien", 1937, 4.7),
    Book("Dune", "Frank Herbert", 1965),
    Book("Emma", "Jane Austen", 1815, 4.2),
]
best = best_rated(shelf)
if best is not None:
    print(best.title, best.rating)
print(best_rated([Book("Dune", "Frank Herbert", 1965)]))
```

Output:

```text
The Hobbit 4.7
None
```

The Hobbit wins with 4.7; Dune is ignored because it has no rating. A shelf with only unrated books gives `None`. The `if best is not None:` check is the same narrowing as in the chapter.

## Exercise 18.5

*Run `ruff check`, `ruff check --fix` and `ruff format` on the messy `Shipping_Cost` function.*

The file `shipping.py`:

```python
import os,sys
def Shipping_Cost( Weight,express ):
  if express==True : return Weight*2.5+10
  else : return Weight*2.5
```

```bash
ruff check --output-format concise shipping.py
```

```output
shipping.py:1:1: I001 [*] Import block is un-sorted or un-formatted
shipping.py:1:8: F401 [*] `os` imported but unused
shipping.py:1:11: F401 [*] `sys` imported but unused
Found 3 errors.
[*] 3 fixable with the `--fix` option.
```

`ruff` reports only the imports. Its default rules aim at likely bugs, and leave naming and comparisons such as `== True` to rules you can switch on. `ruff check --fix` removes the import line (`Found 2 errors (2 fixed, 0 remaining).`, because removing the line also settles the sorting problem), and `ruff format shipping.py` reports `1 file reformatted` and rewrites the layout:

```python
def Shipping_Cost(Weight, express):
    if express == True:
        return Weight * 2.5 + 10
    else:
        return Weight * 2.5
```

Four-space indentation, spaces around operators and one statement per line: the formatter did everything about layout. The names and the logic are still yours to fix. Extra rule groups show them: `E` (the rules of the `pycodestyle` tool, which checks PEP 8) and `N` (PEP 8 naming):

```bash
ruff check --extend-select E,N --output-format concise shipping.py
```

```output
shipping.py:1:5: N802 Function name `Shipping_Cost` should be lowercase
shipping.py:1:19: N803 Argument name `Weight` should be lowercase
shipping.py:2:8: E712 Avoid equality comparisons to `True`; use `express:` for truth checks
Found 3 errors.
No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
```

To use these rules every time, put them in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 79

[tool.ruff.lint]
extend-select = ["E", "N"]
```

Renaming is never automatic, because other code may call the function by its old name. Fixed by hand, with constants for the magic numbers and type hints, the file is the chapter's clean version:

```python
PRICE_PER_KG = 2.5
EXPRESS_FEE = 10


def shipping_cost(weight_kg: float, express: bool = False) -> float:
    """Return the shipping cost of a parcel in dollars."""
    cost = weight_kg * PRICE_PER_KG
    if express:
        cost += EXPRESS_FEE
    return cost
```

With the `pyproject.toml` above in the folder, `ruff check` reports `All checks passed!`.

## Exercise 18.6

*Refactor the order-price function `p` into small, hinted functions, prove that the results are unchanged, and run `mypy`.*

The original, with its one long line wrapped in parentheses so that it fits:

```python
def p(o):
    return (sum(o) * 0.9 if sum(o) > 100
            else sum(o) + 5 if sum(o) < 20 else sum(o))

cases = [[], [10], [19.99], [20], [50, 50], [100], [100.01],
         [60, 70], [5, 5, 5]]
expected = [p(case) for case in cases]
print(expected)
```

Output:

```text
[5, 15, 24.99, 20, 100, 100, 90.009, 117.0, 20]
```

The cases sit on both sides of each boundary: 19.99 and 20 for the fee, 100 and 100.01 for the discount, plus an empty order and orders of several items. An order of exactly 100 pays 100, because the discount starts above 100, while 100.01 pays 90.009, and 19.99 pays 24.99 with the fee. The empty order costs 5, because its sum is 0, below 20: odd perhaps, but the refactoring must keep it, and the characterization test records it. The refactored version, as in `order_price.py`:

```python
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
```

```python
def order_total(prices: list[float]) -> float:
    """Return what the customer pays for items with these prices."""
    return amount_due(sum(prices))

for case, old in zip(cases, expected):
    assert order_total(case) == old, case
print("all", len(cases), "cases unchanged")
```

Output:

```text
all 9 cases unchanged
```

All 9 cases give exactly the same results. The changes: the one-letter names became `prices` and `subtotal`; the sum is computed once instead of up to five times; the magic numbers became constants; and the nested conditional expression became two early returns that read like the rules. Splitting off `amount_due` means the rules can be tested with a single number. `1 - DISCOUNT_RATE` is exactly `0.9` in floating point, so even the float results are identical, which the `==` in the `assert` confirms. Running `python -m mypy order_price.py` reports `Success: no issues found in 1 source file`.
