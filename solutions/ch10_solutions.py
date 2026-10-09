"""Solutions to the Chapter 10 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch10_solutions.py

The explanations are in ch10_solutions.md."""

# %% Exercise 10.1
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

# %% Exercise 10.2
def ask_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Please enter a number.")

print(ask_float("A number: "))
print(ask_float("Another: "))

# %% Exercise 10.3
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

# %% Exercise 10.4
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

# %% Exercise 10.5
# This example stops with an error on purpose (see the book).
try:
    def middle(items):
        return items[len(items) / 2]

    print(middle([1, 2, 3]))
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% Exercise 10.5
def middle(items):
    """Return the middle item (the later one of two, for even lengths)."""
    if not items:
        raise ValueError("middle() of an empty list")
    return items[len(items) // 2]

print(middle([1, 2, 3]), middle(["a", "b", "c", "d"]))

# %% Exercise 10.6
def count_long(text, n):
    count = 0
    for w in text.split():
        print(f"  {w=} {len(w)=} {len(w) >= n=}")
        if len(w) >= n:
            count += 1
    return count

print(count_long("a bb ccc dddd", 2))

# %% Exercise 10.7
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

# %% Exercise 10.7
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
