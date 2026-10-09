"""Chapter 8: Functions

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch08_functions.py

The script asks you to type answers. To replay the answers used
in the book instead:

    python ch08_functions.py < ch08_functions.inputs.txt

You can also open the notebook and run the cells in order.
"""

# %% 8.1 Defining and calling a function
def greet():
    print("Hello!")
    print("Welcome to Python for All.")

greet()
greet()

# %% 8.2 Parameters and arguments
def greet(name, greeting):
    print(f"{greeting}, {name}!")

greet("Ravi", "Good morning")
greet("Mei", "Hi")

# %% 8.2 Parameters and arguments
# This example stops with an error on purpose (see the book).
try:
    def greet(name, greeting):
        print(f"{greeting}, {name}!")

    greet("Ravi")
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% 8.3 Returning values
def area(width, height):
    return width * height

room = area(4, 3.5)
print(room)
print(area(2, 2) + area(3, 1))

# %% 8.3 Returning values
def shout(text):
    print(text.upper())

result = shout("hello")
print(result)

# %% 8.3 Returning values
def grade(score):
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    return "F"

print(grade(95), grade(85), grade(42))

# %% 8.3 Returning values
def min_max_avg(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

low, high, avg = min_max_avg([4, 8, 15, 16, 23, 42])
print(low, high, avg)

# %% 8.4 Default values and keyword arguments
def power(base, exponent=2):
    return base ** exponent

print(power(5), power(5, 3))
print(power(exponent=3, base=2))

# %% 8.5 Scope: where variables live
rate = 0.08

def with_tax(price):
    tax = price * rate
    return price + tax

print(with_tax(50))
print("rate is still", rate)

# %% 8.5 Scope: where variables live
# This example stops with an error on purpose (see the book).
try:
    total = 0

    def add(amount):
        total = total + amount

    add(5)
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% 8.5 Scope: where variables live
def add(total, amount):
    return total + amount

total = 0
total = add(total, 5)
total = add(total, 10)
print(total)

# %% 8.6 Flexible arguments: args and kwargs
def average(*numbers):
    return sum(numbers) / len(numbers)

print(average(3, 4))
print(average(10, 20, 30, 40))
values = [2, 4, 9]
print(average(*values))

# %% 8.6 Flexible arguments: args and kwargs
def describe(name, **details):
    print(name)
    for key, value in details.items():
        print(f"  {key}: {value}")

describe("Mount Everest", height_m=8849, country="Nepal/China")

# %% 8.7 Documenting functions
def bmi(weight, height):
    """Return the body mass index.

    weight is in kilograms and height in meters.
    """
    return weight / height ** 2

help(bmi)
print(round(bmi(70, 1.75), 1))

# %% 8.7 Documenting functions
def bmi(weight: float, height: float) -> float:
    """Return the body mass index (kg and meters)."""
    return weight / height ** 2

print(f"{bmi(70, 1.75):.1f}")

# %% 8.8 Functions are values
def last_letter(word):
    return word[-1]

words = ["banana", "kiwi", "apple", "fig"]
print(sorted(words, key=last_letter))

# %% 8.8 Functions are values
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

operations = {"+": add, "*": multiply}
print(operations["*"](6, 7))

# %% 8.9 Putting it together: a reusable input helper
def ask_int(prompt, low, high):
    """Ask until the user types a whole number from low to high."""
    while True:
        text = input(prompt).strip()
        if text.isdigit() and low <= int(text) <= high:
            return int(text)
        print(f"  Please enter a whole number from {low} to {high}.")

age = ask_int("Your age: ", 0, 120)
print("Thank you. Next year you will be", age + 1)

# %% 8.9 Putting it together: a reusable input helper
def split_bill(bill, tip_percent, people):
    """Return the tip, the total and each person's share."""
    tip = bill * tip_percent / 100
    total = bill + tip
    return tip, total, total / people

def main():
    bill = ask_int("Bill amount ($): ", 1, 10_000)
    tip_percent = ask_int("Tip (%): ", 0, 100)
    people = ask_int("Number of people: ", 1, 50)
    tip, total, share = split_bill(bill, tip_percent, people)
    print(f"Tip ${tip:.2f}, total ${total:.2f}, "
          f"each pays ${share:.2f}")

main()
