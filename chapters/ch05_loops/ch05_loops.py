"""Chapter 5: Repeating Work with Loops

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch05_loops.py

The script asks you to type answers. To replay the answers used
in the book instead:

    python ch05_loops.py < ch05_loops.inputs.txt

You can also open the notebook and run the cells in order.
"""

# %% 5.1 The while loop
count = 3
while count > 0:
    print(count, "...")
    count -= 1
print("Liftoff!")

# %% 5.1 The while loop
answer = input("How many days in a week? ")
while not answer.isdigit():
    print("Please type the number using digits.")
    answer = input("How many days in a week? ")
days = int(answer)
print("Hours in a week:", days * 24)

# %% 5.1 The while loop
total = 0
count = 0
price = input("Price (blank to finish): ")
while price != "":
    total += float(price)
    count += 1
    price = input("Price (blank to finish): ")
print(f"{count} items, total ${total:.2f}")

# %% 5.2 The for loop
for letter in "Python":
    print(letter, end=" ")
print()

# %% 5.2 The for loop
sentence = "Programming in Python is fun"
vowels = 0
for ch in sentence.lower():
    if ch in "aeiou":
        vowels += 1
print(f"{vowels} vowels in {len(sentence)} characters")

# %% 5.3 Counting with range
for i in range(5):
    print(i, end=" ")
print()
for i in range(1, 6):
    print(i, end=" ")
print()
for i in range(0, 20, 5):
    print(i, end=" ")
print()
for i in range(10, 0, -3):
    print(i, end=" ")
print()

# %% 5.3 Counting with range
for _ in range(3):
    print("Hip hip hooray!")

# %% 5.3 Counting with range
total = 0
for n in range(1, 101):
    total += n
print("Sum of 1 to 100:", total)

# %% 5.3 Counting with range
temps = "18 23 17 29 25"
highest = None
report = ""
for t in temps.split():
    t = int(t)
    if highest is None or t > highest:
        highest = t
    report += "*" * (t // 5) + " "
print("Highest:", highest)
print(report)

# %% 5.4 Changing the flow: break and continue
for n in range(1, 20):
    if n % 7 == 0:
        print("First multiple of 7:", n)
        break
for n in range(1, 11):
    if n % 3 == 0:
        continue
    print(n, end=" ")
print()

# %% 5.4 Changing the flow: break and continue
while True:
    reply = input("Continue? (y/n) ").strip().lower()
    if reply in ("y", "n"):
        break
    print("Please answer y or n.")
print("You chose:", reply)

# %% 5.5 Nested loops
for row in range(1, 6):
    for col in range(1, 6):
        print(f"{row * col:4}", end="")
    print()

# %% 5.5 Nested loops
for row in range(1, 5):
    print("*" * row)
for row in range(1, 5):
    spaces = " " * (4 - row)
    print(spaces + "* " * row)

# %% 5.6 Random numbers
import random

random.seed(42)
print(random.randint(1, 6), random.randint(1, 6))
print(random.choice("ABCD"), random.random())

# %% 5.6 Random numbers
random.seed(7)
for game in range(1, 6):
    rolls = 1
    while random.randint(1, 6) != 6:
        rolls += 1
    word = "roll" if rolls == 1 else "rolls"
    print(f"Game {game}: a six after {rolls} {word}")

# %% 5.7 Putting it together: a times-table quiz
import random
random.seed(3)
score = 0
for question in range(1, 6):
    a, b = random.randint(2, 9), random.randint(2, 9)
    while True:
        answer = input(f"Q{question}: {a} x {b} = ").strip()
        if answer.isdigit():
            break
        print("  Please type a number.")
    if int(answer) == a * b:
        score += 1
        print("  Correct!")
    else:
        print(f"  Not quite: {a} x {b} = {a * b}")
print(f"You scored {score} out of 5.")
