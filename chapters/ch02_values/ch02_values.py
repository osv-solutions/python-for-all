"""Chapter 2: Values, Variables and Types

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch02_values.py

The script asks you to type answers. To replay the answers used
in the book instead:

    python ch02_values.py < ch02_values.inputs.txt

You can also open the notebook and run the cells in order.
"""

# %% 2.1 Every value has a type
print(type(42))
print(type(3.14))
print(type("hello"))
print(type(True))
print(type(None))

# %% 2.2 Numbers and arithmetic
print(17 / 5)
print(17 // 5)
print(17 % 5)
print(10 / 2)

# %% 2.2 Numbers and arithmetic
print(14 % 2, 15 % 2)
minutes = 135
print(minutes // 60, "hours and", minutes % 60, "minutes")

# %% 2.2 Numbers and arithmetic
print(2 + 3 * 4)
print((2 + 3) * 4)
print(2 * 3 ** 2)
print(-2 ** 2, (-2) ** 2)

# %% 2.2 Numbers and arithmetic
print(2 ** 100)
population = 8_100_000_000
print(population)
print(7 + 2.0, 3 * 1.5)

# %% 2.2 Numbers and arithmetic
print(0.1 + 0.2)
print(round(0.1 + 0.2, 2))
print(round(3.14159, 3), round(2.5), round(3.5))

# %% 2.3 Variables
price = 4.50
quantity = 3
total = price * quantity
print(total)

# %% 2.3 Variables
score = 10
best = score
score = 25
print("score:", score, " best:", best)

# %% 2.3 Variables
lives = 3
lives = lives - 1
print(lives)
lives -= 1
print(lives)
points = 100
points *= 2
print(points)

# %% 2.3 Variables
# This example contains a mistake on purpose (see the book).
# Python would refuse to run this whole file, so it is commented
# out. Copy it into a file of its own to see the error message:
# 2nd_place = "Ravi"


# %% 2.4 Strings, a first look
city = "Visakhapatnam"
quote = 'She said "hello" and left.'
greeting = "Hello, " + city + "!"
print(greeting)
print(quote)
print("-" * 20)
print(len(city))

# %% 2.4 Strings, a first look
# This example stops with an error on purpose (see the book).
try:
    age = 30
    print("You are " + age + " years old.")
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% 2.5 Booleans and None
is_raining = False
print(is_raining)
print(5 > 3, 2 + 2 == 5)

# %% 2.5 Booleans and None
winner = None
print(winner)
result = print("This line is printed.")
print(result)

# %% 2.6 Getting input from the user
name = input("What is your name? ")
print("Nice to meet you,", name)

# %% 2.6 Getting input from the user
# This example stops with an error on purpose (see the book).
try:
    age = input("How old are you? ")
    print("Next year you will be", age + 1)
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% 2.7 Converting between types
print(int("41") + 1)
print(float("3.75") * 2)
print(str(2026) + "!")
print(int(9.99), round(9.99))
print(float(3))

# %% 2.7 Converting between types
# This example stops with an error on purpose (see the book).
try:
    print(float("3.5"))
    print(int("3.5"))
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% 2.7 Converting between types
age = int(input("How old are you? "))
print("Next year you will be", age + 1)

# %% 2.8 Putting it together: a tip calculator
bill = float(input("Bill amount: $"))
tip_percent = int(input("Tip (%): "))
people = int(input("Number of people: "))

tip = bill * tip_percent / 100
total = bill + tip
per_person = total / people

print("Tip:", round(tip, 2))
print("Total:", round(total, 2))
print("Each person pays:", round(per_person, 2))

# %% 2.8 Putting it together: a tip calculator
print(f"Each person pays: ${per_person:.2f}")
print(f"{people} people, {tip_percent}% tip on ${bill}")
