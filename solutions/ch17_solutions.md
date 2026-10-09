# Solutions: Chapter 17, Testing Your Code with pytest

Worked solutions to the exercises at the end of Chapter 17 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch17_solutions.ipynb`](ch17_solutions.ipynb) or the script `ch17_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

The solution files are in `examples/ch17_solutions/` in the companion repository. Run all of them from that folder with `python -m pytest`; all 32 tests pass. The folder holds copies of `tickets.py` and `cart.py` from Chapter 17 for Exercise 17.3.

## Exercise 17.1

*Write `test_average.py` with three tests for `average`, one of them for floats with `pytest.approx`.*

The function goes in its own module, so that the tests can import it:

```python
def average(numbers):
    return sum(numbers) / len(numbers)
```

The tests:

```python
import pytest

from average import average


def test_whole_numbers():
    assert average([2, 4, 6]) == 4


def test_single_number():
    assert average([5]) == 5


def test_floats():
    assert average([0.1, 0.2, 0.3]) == pytest.approx(0.2)
```

`0.1 + 0.2 + 0.3` is `0.6000000000000001` in floating point, and divided by 3 it isn't exactly `0.2`, so `==` would fail although `average` is right. `pytest.approx(0.2)` accepts the tiny rounding error. Running `python -m pytest -v test_average.py` lists each test by name (shown here after the header, with the test of Exercise 17.2 already added):

```output
test_average.py::test_whole_numbers PASSED                           [ 25%]
test_average.py::test_single_number PASSED                           [ 50%]
test_average.py::test_floats PASSED                                  [ 75%]
test_average.py::test_empty_list_raises PASSED                       [100%]

============================ 4 passed in 0.01s =============================
```

## Exercise 17.2

*Test that `average([])` raises a `ZeroDivisionError`.*

```python
def test_empty_list_raises():
    with pytest.raises(ZeroDivisionError):
        average([])
```

`sum([])` is 0 and `len([])` is 0, so the function divides 0 by 0. The test documents this behavior: anyone who later decides that the average of an empty list should be `None`, or raise a `ValueError` with a clearer message, will see this test fail and update it on purpose rather than by accident.

## Exercise 17.3

*Write tests for the two lines that the coverage report showed as untested.*

```python
import pytest

from cart import Cart
from tickets import split_bill


def test_cart_rejects_negative_price():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add("pen", -1.50)


def test_split_bill_needs_people():
    with pytest.raises(ValueError, match="at least 1"):
        split_bill(100, 10, 0)
```

The first test builds its own cart and checks that a negative price is refused; the second checks both the exception and its message. With this file added to the chapter's folder, `python -m pytest --cov --cov-report=term-missing` reports 100% for every file:

```output
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
cart.py              20      0   100%
prices.py             3      0   100%
test_cart.py         25      0   100%
test_gaps.py         10      0   100%
test_prices.py       11      0   100%
test_tickets.py      24      0   100%
tickets.py           14      0   100%
-----------------------------------------------
TOTAL               107      0   100%
```

Tests for error handling are easy to forget, because the code works in the normal case, but the error paths are exactly where surprises hide.

## Exercise 17.4

*Write a parametrized test for `grade(score)` with boundary values, then write the function.*

Following the order of the exercise, the test comes first:

```python
import pytest

from grade import grade


@pytest.mark.parametrize("score, letter", [
    (100, "A"), (90, "A"), (89, "B"), (80, "B"),
    (79, "C"), (70, "C"), (69, "F"), (0, "F"),
])
def test_grade(score, letter):
    assert grade(score) == letter
```

Each boundary is tested from both sides: 90 and 89, 80 and 79, 70 and 69, plus the extremes 100 and 0. Running it before `grade.py` exists fails with a `ModuleNotFoundError`, the red step. Then the function:

```python
def grade(score):
    """Return the letter grade for a score from 0 to 100."""
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    return "F"
```

The checks run from the highest grade down, so each `if` only needs a lower limit: a score that reaches the second `if` is already known to be below 90. All eight cases pass:

```output
test_grade.py::test_grade[100-A] PASSED                              [ 12%]
test_grade.py::test_grade[90-A] PASSED                               [ 25%]
test_grade.py::test_grade[89-B] PASSED                               [ 37%]
test_grade.py::test_grade[80-B] PASSED                               [ 50%]
test_grade.py::test_grade[79-C] PASSED                               [ 62%]
test_grade.py::test_grade[70-C] PASSED                               [ 75%]
test_grade.py::test_grade[69-F] PASSED                               [ 87%]
test_grade.py::test_grade[0-F] PASSED                                [100%]

============================ 8 passed in 0.02s =============================
```

If `>= 90` had been written as `> 90`, only the case `[90-A]` would fail, and its name would point straight at the mistake.

## Exercise 17.5

*Write `word_count(path)` and test it with `tmp_path`, with a short file and an empty one.*

```python
def word_count(path):
    """Return the number of words in a text file."""
    return len(path.read_text(encoding="utf-8").split())
```

```python
from words import word_count


def test_short_file(tmp_path):
    path = tmp_path / "poem.txt"
    path.write_text("The rain in Spain\nfalls mainly\n")
    assert word_count(path) == 6


def test_empty_file(tmp_path):
    path = tmp_path / "empty.txt"
    path.write_text("")
    assert word_count(path) == 0
```

Each test writes its own file into its own temporary folder, so the tests never depend on files on your computer, and they can't overwrite anything. The short file has six words over two lines: `split()` with no argument splits at any whitespace, line breaks included. The empty file gives `[]`, of length 0. Both tests pass.

## Exercise 17.6

*Build `is_valid_username(name)` test-first: 3 to 15 characters, only letters, digits and underscores, not starting with a digit.*

Working test-first, one rule at a time, the steps were:

1. A test that `"ada"` is valid, with a function that just returns `True`: green at once.

2. A test that `"ab"` is invalid: red. The function now returns `3 <= len(name) <= 15`: green, and a test for 16 characters passes too.

3. Tests for `"has space"` and `"dash-name"`: red. Add the check that every character is a letter, a digit or an underscore: green.

4. A test for `"9lives"`: red. Add the check on the first character: green.

5. Refactor: turn the separate tests into two parametrized tests, one for valid names and one for invalid ones, and add the empty string.

The final tests and function:

```python
import pytest

from usernames import is_valid_username


@pytest.mark.parametrize("name", [
    "ada", "grace_hopper", "x_1", "a" * 15,
])
def test_valid(name):
    assert is_valid_username(name)


@pytest.mark.parametrize("name", [
    "ab", "a" * 16, "has space", "dash-name", "9lives", "",
])
def test_invalid(name):
    assert not is_valid_username(name)
```

```python
def is_valid_username(name):
    """3-15 letters, digits or _, not starting with a digit."""
    return (3 <= len(name) <= 15
            and all(c.isalnum() or c == "_" for c in name)
            and not name[0].isdigit())
```

`isalnum()` is true for letters and digits. The order of the conditions matters for the empty string: `and` stops at the first false condition, so for `""` the length check fails before `name[0]` is evaluated, which would raise an `IndexError`. Without the test for `""`, that trap would be easy to fall into. All ten cases pass:

```output
test_usernames.py::test_valid[ada] PASSED                            [ 10%]
test_usernames.py::test_valid[grace_hopper] PASSED                   [ 20%]
test_usernames.py::test_valid[x_1] PASSED                            [ 30%]
test_usernames.py::test_valid[aaaaaaaaaaaaaaa] PASSED                [ 40%]
test_usernames.py::test_invalid[ab] PASSED                           [ 50%]
test_usernames.py::test_invalid[aaaaaaaaaaaaaaaa] PASSED             [ 60%]
test_usernames.py::test_invalid[has space] PASSED                    [ 70%]
test_usernames.py::test_invalid[dash-name] PASSED                    [ 80%]
test_usernames.py::test_invalid[9lives] PASSED                       [ 90%]
test_usernames.py::test_invalid[] PASSED                             [100%]

============================ 10 passed in 0.02s ============================
```

`isalnum` also accepts letters from other alphabets, such as `é` or `ж`. If only the English letters should be allowed, test for that first, then change the check.

## Exercise 17.7

*Test the `BankAccount` of Chapter 12 with a fixture: deposits, withdrawals, refusing to overdraw and refusing bad deposits.*

The class from Chapter 12, with its read-only `balance` property, goes into `bank.py`:

```python
"""The BankAccount of Chapter 12, with a read-only balance."""


class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount
```

```python
import pytest

from bank import BankAccount


@pytest.fixture
def account():
    return BankAccount("Asha", 100)


def test_deposit(account):
    account.deposit(50)
    assert account.balance == 150


def test_withdraw(account):
    account.withdraw(30)
    assert account.balance == 70
```

The fixture gives each test a fresh account with a balance of 100, so `test_withdraw` doesn't see the deposit made by `test_deposit`. The refusals:

```python
def test_overdraw_is_refused(account):
    with pytest.raises(ValueError, match="insufficient"):
        account.withdraw(500)
    assert account.balance == 100


@pytest.mark.parametrize("amount", [0, -1, -50.5])
def test_bad_deposit_is_refused(account, amount):
    with pytest.raises(ValueError):
        account.deposit(amount)
    assert account.balance == 100
```

Both tests check two things: that the error is raised, *and* that the balance is unchanged afterward. A method that changed the balance before raising the error would pass the first check but fail the second. A test function can use a fixture and parametrize together: `test_bad_deposit_is_refused` gets a fresh account for each of the three amounts.

```output
test_bank.py::test_deposit PASSED                                    [ 16%]
test_bank.py::test_withdraw PASSED                                   [ 33%]
test_bank.py::test_overdraw_is_refused PASSED                        [ 50%]
test_bank.py::test_bad_deposit_is_refused[0] PASSED                  [ 66%]
test_bank.py::test_bad_deposit_is_refused[-1] PASSED                 [ 83%]
test_bank.py::test_bad_deposit_is_refused[-50.5] PASSED              [100%]

============================ 6 passed in 0.01s =============================
```
