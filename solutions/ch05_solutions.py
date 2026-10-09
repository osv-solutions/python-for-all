"""Solutions to the Chapter 5 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch05_solutions.py

The explanations are in ch05_solutions.md."""

# %% Exercise 5.1
n = 2
while n <= 20:
    print(n, end=" ")
    n += 2
print()
for n in range(2, 21, 2):
    print(n, end=" ")
print()

# %% Exercise 5.2
word = input("Word: ")
number = 1
for letter in word:
    print(f"{number}: {letter}")
    number += 1

# %% Exercise 5.3
n = int(input("n: "))
factorial = 1
for k in range(2, n + 1):
    factorial *= k
print(f"{n}! = {factorial:,}")

# %% Exercise 5.4
count = 0
total = 0
highest = lowest = None
while True:
    text = input("Score (blank to finish): ").strip()
    if text == "":
        break
    score = float(text)
    count += 1
    total += score
    if highest is None or score > highest:
        highest = score
    if lowest is None or score < lowest:
        lowest = score
if count == 0:
    print("No scores entered.")
else:
    print(f"{count} scores, average {total / count:.1f}, "
          f"highest {highest}, lowest {lowest}")

# %% Exercise 5.5
print("   |", end="")
for col in range(1, 11):
    print(f"{col:4}", end="")
print()
print("---+" + "-" * 40)
for row in range(1, 11):
    print(f"{row:2} |", end="")
    for col in range(1, 11):
        print(f"{row * col:4}", end="")
    print()

# %% Exercise 5.6
import random

random.seed(1)
sevens = 0
for _ in range(1000):
    total = random.randint(1, 6) + random.randint(1, 6)
    if total == 7:
        sevens += 1
print(f"{sevens} sevens in 1,000 rolls ({sevens / 1000:.1%})")
print(f"expected about {1000 / 6:.0f} ({1 / 6:.1%})")

# %% Exercise 5.7
for n in range(1, 31):
    if n % 15 == 0:
        print("FizzBuzz", end=" ")
    elif n % 3 == 0:
        print("Fizz", end=" ")
    elif n % 5 == 0:
        print("Buzz", end=" ")
    else:
        print(n, end=" ")
print()

# %% Exercise 5.7
line = ""
for n in range(1, 31):
    if n % 15 == 0:
        word = "FizzBuzz"
    elif n % 3 == 0:
        word = "Fizz"
    elif n % 5 == 0:
        word = "Buzz"
    else:
        word = str(n)
    if line:
        line += ", "
    line += word
print(line)
