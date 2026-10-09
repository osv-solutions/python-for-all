"""Project 1 (Beginner): Number Guessing Game

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python p01_guessing_game.py

The script asks you to type answers. To replay the answers used
in the book instead:

    python p01_guessing_game.py < p01_guessing_game.inputs.txt

You can also open the notebook and run the cells in order.
"""

# %% Step 2: Pick a secret number
import random

random.seed(12)  # for testing: the same secret every run
secret = random.randint(1, 100)
print("(testing) the secret is", secret)

# %% Step 3: One guess, one hint
guess = int(input("Your guess: "))
if guess < secret:
    print("Too low.")
elif guess > secret:
    print("Too high.")
else:
    print("Correct!")

# %% Step 4: Keep guessing
random.seed(12)
secret = random.randint(1, 100)
tries = 0
guess = 0
while guess != secret:
    guess = int(input("Your guess: "))
    tries += 1
    if guess < secret:
        print("  Too low.")
    elif guess > secret:
        print("  Too high.")
print(f"Correct! You found {secret} in {tries} tries.")

# %% Step 5: Handle bad input
random.seed(12)
secret = random.randint(1, 100)
tries = 0
guess = 0
while guess != secret:
    text = input("Your guess: ").strip()
    if not text.isdigit() or not 1 <= int(text) <= 100:
        print("  Please enter a whole number from 1 to 100.")
        continue
    guess = int(text)
    tries += 1
    if guess < secret:
        print("  Too low.")
    elif guess > secret:
        print("  Too high.")
print(f"Correct! You found {secret} in {tries} tries.")

# %% Step 6: Limit the number of tries
random.seed(12)
secret = random.randint(1, 100)
max_tries = 7
tries = 0

# %% Step 6: Limit the number of tries
while tries < max_tries:
    text = input(f"Guess {tries + 1} of {max_tries}: ").strip()
    guess = int(text) if text.isdigit() else 0
    if not 1 <= guess <= 100:
        print("  Please enter a whole number from 1 to 100.")
        continue
    tries += 1
    if guess < secret:
        print("  Too low.")
    elif guess > secret:
        print("  Too high.")
    else:
        print(f"  Correct! You found it in {tries} tries.")
        break
else:
    print(f"Out of tries! The number was {secret}.")

# %% Step 7: Difficulty levels
level = input("Difficulty (easy, normal, hard): ").strip().lower()
match level:
    case "easy":
        top, max_tries = 20, 5
    case "hard":
        top, max_tries = 1000, 10
    case _:
        level = "normal"
        top, max_tries = 100, 7
print(f"Level {level}: a number from 1 to {top}, "
      f"{max_tries} tries.")

# %% Step 7: Difficulty levels
random.seed(7)  # same game every run; delete this line to play
secret = random.randint(1, top)
tries = 0

# %% Step 7: Difficulty levels
while tries < max_tries:
    text = input(f"Guess {tries + 1} of {max_tries}: ").strip()
    guess = int(text) if text.isdigit() else 0
    if not 1 <= guess <= top:
        print(f"  Please enter a whole number from 1 to {top}.")
        continue
    tries += 1
    if guess < secret:
        print("  Too low.")
    elif guess > secret:
        print("  Too high.")
    else:
        print(f"  Correct! You found it in {tries} tries.")
        break
else:
    print(f"Out of tries! The number was {secret}.")
