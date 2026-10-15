# Solutions: Chapter 10, Errors, Exceptions and Debugging

Worked solutions to the exercises at the end of Chapter 10 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch10_solutions.ipynb`](ch10_solutions.ipynb) or the script `ch10_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 10.1

*Trigger a `ValueError`, a `ZeroDivisionError`, an `IndexError` and a `KeyError`, catching each and printing its message.*

```python
try:
    int("ten")
except ValueError as err:
    print("ValueError:", err)
try:
    print(1 / 0)
except ZeroDivisionError as err:
    print("ZeroDivisionError:", err)
try:
    print([1, 2, 3][10])
except IndexError as err:
    print("IndexError:", err)
try:
    print({"a": 1}["b"])
except KeyError as err:
    print("KeyError:", err)
```

Output:

```text
ValueError: invalid literal for int() with base 10: 'ten'
ZeroDivisionError: division by zero
IndexError: list index out of range
KeyError: 'b'
```

Each `try` holds one operation that is certain to fail, and each `except` names the exact exception it expects. The message of a `KeyError` is just the missing key, `'b'`, which is why programs often add their own explanation when they report one.

## Exercise 10.2

*Write `ask_float(prompt)` with `try` and `except`, and test it with `abc`, `2.5e3` and `-7`.*

```python
def ask_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Please enter a number.")

print(ask_float("A number: "))
print(ask_float("Another: "))
```

Output:

```text
A number: abc
  Please enter a number.
A number: 2.5e3
2500.0
Another: -7
-7.0
```

`return float(input(prompt))` either returns a number, ending the loop and the function, or raises a `ValueError`, which leads to the hint and another try. `float` accepts more than the string checks of Chapter 8: `2.5e3` is scientific notation for 2,500, and negative numbers work too.

## Exercise 10.3

*Write `parse_date(text)` that turns `"DD/MM/YYYY"` into a `date`, with a helpful error for the wrong shape.*

```python
from datetime import date

def parse_date(text):
    parts = text.strip().split("/")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise ValueError(f"expected DD/MM/YYYY, got {text!r}")
    day, month, year = (int(p) for p in parts)
    return date(year, month, day)

for text in ["08/10/2026", "8-10-2026", "31/02/2026"]:
    try:
        print(parse_date(text))
    except ValueError as err:
        print("Error:", err)
```

Output:

```text
2026-10-08
Error: expected DD/MM/YYYY, got '8-10-2026'
Error: day 31 must be in range 1..28 for month 2 in year 2026
```

The shape check raises our own message for text such as `8-10-2026`. `all(...)` is a built-in function that is true when every item is true (Chapter 14); here it checks that each part contains only digits. A date with the right shape but impossible values, such as February 31, gets through the check, and then `date` itself raises a `ValueError` with its own message.

## Exercise 10.4

*Total an order, skipping and reporting unknown items, first with `try`/`except KeyError`, then with `get`.*

```python
prices = {"tea": 2.5, "cake": 3.75}
order = ["tea", "pie", "cake", "tea"]
total = 0
for item in order:
    try:
        total += prices[item]
    except KeyError:
        print("Unknown item:", item)
print(f"Total: ${total:.2f}")
total = 0
for item in order:
    price = prices.get(item)
    if price is None:
        print("Unknown item:", item)
    else:
        total += price
print(f"Total: ${total:.2f}")
```

Output:

```text
Unknown item: pie
Total: $8.75
Unknown item: pie
Total: $8.75
```

Both versions give $8.75 and report the pie. Here the `try` version is slightly shorter and reads naturally: try to add the price, and deal with the rare unknown item. The `get` version is better if a missing item is common, or if you want to treat it as free with `prices.get(item, 0)`.

## Exercise 10.5

*Fix `middle(items)`, and make it raise a clear `ValueError` for an empty list.*

```python
def middle(items):
    return items[len(items) / 2]

print(middle([1, 2, 3]))
```

Output:

```text
Traceback (most recent call last):
  File "C:\Users\ada\Documents\python-for-all\middle.py", line 4, in <module>
    print(middle([1, 2, 3]))
          ~~~~~~^^^^^^^^^^^
  File "C:\Users\ada\Documents\python-for-all\middle.py", line 2, in middle
    return items[len(items) / 2]
           ~~~~~^^^^^^^^^^^^^^^^
TypeError: list indices must be integers or slices, not float
```

The traceback says that list indices must be integers, not floats: `/` always gives a float (Chapter 2), so `3 / 2` is `1.5`. Floor division gives the whole-number index:

```python
def middle(items):
    """Return the middle item (the later one of two, for even lengths)."""
    if not items:
        raise ValueError("middle() of an empty list")
    return items[len(items) // 2]

print(middle([1, 2, 3]), middle(["a", "b", "c", "d"]))
```

Output:

```text
2 c
```

`3 // 2` is 1, the index of the middle of three items. For an empty list, `len(items) // 2` would be 0 and `items[0]` would raise an `IndexError`, which doesn't explain the real problem, so the function checks first and raises a clear `ValueError` instead.

## Exercise 10.6

*Find and fix the bug in `count_long`.*

```python
def count_long(text, n):
    count = 0
    for w in text.split():
        print(f"  {w=} {len(w)=} {len(w) >= n=}")
        if len(w) >= n:
            count += 1
    return count

print(count_long("a bb ccc dddd", 2))
```

Output:

```text
  w='a' len(w)=1 len(w) >= n=False
  w='bb' len(w)=2 len(w) >= n=True
  w='ccc' len(w)=3 len(w) >= n=True
  w='dddd' len(w)=4 len(w) >= n=True
3
```

Words *longer than* 2 letters are `ccc` and `dddd`, so the answer should be 2, but the function returns 3. The debugging print shows that `bb`, with exactly 2 letters, passes the test `len(w) >= n`. The condition should be `len(w) > n`: "longer than" excludes the boundary, while `>=` includes it. Boundary mistakes like this are among the most common logic errors (see the In the real world box of Chapter 4).

## Exercise 10.7

*Extend the calculator with `%`, `**`, a memory `m` and a count of failed expressions.*

```python
def calculate(text, memory):
    parts = text.split()
    if len(parts) != 3:
        raise ValueError("write a number, an operator and a number")
    a, op, b = parts
    a = memory if a == "m" else float(a)
    b = memory if b == "m" else float(b)
    match op:
        case "+": return a + b
        case "-": return a - b
        case "*": return a * b
        case "/": return a / b
        case "%": return a % b
        case "**": return a ** b
    raise ValueError(f"unknown operator {op!r}")
```

The letter `m` in place of a number is replaced by the value in memory before the calculation. The loop keeps the memory and the count of failures:

```python
memory, failures = 0.0, 0
while (text := input("> ").strip()) != "q":
    try:
        memory = calculate(text, memory)
    except (ValueError, ZeroDivisionError) as err:
        failures += 1
        print("  Error:", err)
    else:
        print(" ", memory)
print(f"{failures} expression(s) failed.")
```

Output:

```text
> 6 * 7
  42.0
> m / 0
  Error: division by zero
> m - 2
  40.0
> 2 ** 10
  1024.0
> m % 7
  2.0
> x + 1
  Error: could not convert string to float: 'x'
> q
2 expression(s) failed.
```

Every successful result becomes the new memory, so `m - 2` continues from 42. A single `except` can catch several exception types, listed in a tuple. `x + 1` fails because `x` is neither a number nor `m`, and the division by zero fails too: two failures. The message for the division, `division by zero`, comes from Python itself.
