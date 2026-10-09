"""Chapter 10: Errors, Exceptions and Debugging

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch10_errors.py

The script asks you to type answers. To replay the answers used
in the book instead:

    python ch10_errors.py < ch10_errors.inputs.txt

You can also open the notebook and run the cells in order.
"""

# %% 10.2 Catching exceptions: try and except
text = input("How old are you? ")
try:
    age = int(text)
    print("Next year you will be", age + 1)
except ValueError:
    print(f"Sorry, {text!r} is not a whole number.")
print("The program carries on.")

# %% 10.2 Catching exceptions: try and except
while True:
    try:
        number = int(input("Enter a whole number: "))
        break
    except ValueError:
        print("  That isn't a whole number. Try again.")
print("You entered", number)

# %% 10.2 Catching exceptions: try and except
def safe_divide(a, b):
    try:
        return float(a) / float(b)
    except ValueError as err:
        print("Bad number:", err)
    except ZeroDivisionError:
        print("Can't divide by zero.")

print(safe_divide("10", "4"))
print(safe_divide("ten", "4"))
print(safe_divide("10", "0"))

# %% 10.2 Catching exceptions: try and except
for attempt in range(2):
    try:
        n = int(input("Divide 100 by: "))
        result = 100 / n
    except ZeroDivisionError:
        print("  Division by zero!")
    else:
        print("  Result:", result)
    finally:
        print("  (attempt", attempt + 1, "finished)")

# %% 10.3 Tracebacks through functions
# This example stops with an error on purpose (see the book).
try:
    def average(numbers):
        return sum(numbers) / len(numbers)

    def report(name, scores):
        print(name, "average:", average(scores))

    report("Asha", [88, 92])
    report("Ben", [])
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% 10.4 Raising exceptions
def average(numbers):
    """Return the mean of a non-empty list of numbers."""
    if not numbers:
        raise ValueError("average() needs at least one number")
    return sum(numbers) / len(numbers)

try:
    average([])
except ValueError as err:
    print("Problem:", err)

# %% 10.5 Ask permission or ask forgiveness?
stock = {"apples": 12, "pears": 5}
item = "kiwis"
if item in stock:
    print(stock[item])
else:
    print("No", item)
try:
    print(stock[item])
except KeyError:
    print("No", item)

# %% 10.6 Debugging
def average_above(numbers, threshold):
    total = 0
    count = 0
    for n in numbers:
        if n > threshold:
            total += n
        count += 1
    return total / count

print(average_above([10, 50, 60, 70], 40))

# %% 10.6 Debugging
def average_above(numbers, threshold):
    total = 0
    count = 0
    for n in numbers:
        if n > threshold:
            total += n
        count += 1
        print(f"  {n=} {total=} {count=}")
    return total / count

print(average_above([10, 50, 60, 70], 40))

# %% 10.7 Putting it together: a forgiving calculator
def calculate(text):
    """Calculate a number, an operator and a number, as in "6 * 7"."""
    parts = text.split()
    if len(parts) != 3:
        raise ValueError("write a number, an operator and a number")
    a, op, b = float(parts[0]), parts[1], float(parts[2])
    match op:
        case "+": return a + b
        case "-": return a - b
        case "*": return a * b
        case "/": return a / b
    raise ValueError(f"unknown operator {op!r}")

# %% 10.7 Putting it together: a forgiving calculator
while (text := input("> ").strip()) != "q":
    try:
        result = calculate(text)
    except ZeroDivisionError:
        print("  Can't divide by zero.")
    except ValueError as err:
        print("  Error:", err)
    else:
        print(" ", result)
