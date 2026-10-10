"""Project 5 (Beginner): Hangman

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python p05_hangman.py

The script asks you to type answers. To replay the answers used
in the book instead:

    python p05_hangman.py < p05_hangman.inputs.txt

You can also open the notebook and run the cells in order.
"""

# %% Step 1: Words and a secret
import random

WORDS = {
    "animals": ["giraffe", "penguin", "dolphin", "hedgehog", "otter"],
    "fruit": ["banana", "apricot", "mango", "blueberry", "kiwi"],
    "countries": ["portugal", "canada", "kenya", "norway", "japan"],
}
KIND = {"animals": "an animal", "fruit": "a fruit",
        "countries": "a country"}
MAX_WRONG = 6


def choose_word():
    category = random.choice(list(WORDS))
    return category, random.choice(WORDS[category])

# %% Step 1: Words and a secret
random.seed(7)             # for testing: the same word every run
category, secret = choose_word()
print(category, secret)    # a test line; remove it before playing

# %% Step 2: Showing the word
def show_word(secret, guessed):
    shown = []
    for letter in secret:
        if letter in guessed:
            shown.append(letter)
        else:
            shown.append("_")
    return " ".join(shown)


print(show_word("apricot", set()))
print(show_word("apricot", {"a", "o", "e"}))

# %% Step 3: The gallows
GALLOWS = [
    "  +---+\n  |   |\n      |\n      |\n      |\n=======",
    "  +---+\n  |   |\n  O   |\n      |\n      |\n=======",
    "  +---+\n  |   |\n  O   |\n  |   |\n      |\n=======",
    "  +---+\n  |   |\n  O   |\n /|   |\n      |\n=======",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n=======",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n=======",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n=======",
]
print(GALLOWS[3])
print(len(GALLOWS) == MAX_WRONG + 1)

# %% Step 4: Reading a guess
def read_guess(guessed):
    while True:
        guess = input("Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Please type a single letter.")
        elif guess in guessed:
            print(f"You already tried {guess!r}.")
        else:
            return guess

# %% Step 4: Reading a guess
print("Got:", read_guess({"a"}))

# %% Step 5: One game
letters = set("apricot")
guessed = {"a", "e", "o", "s", "t"}
print(sorted(letters & guessed), sorted(guessed - letters))
print(letters <= guessed, letters <= guessed | set("pric"))

# %% Step 5: One game
def play(category, secret):
    letters, guessed, wrong = set(secret), set(), 0
    print(f"The word is {KIND[category]}: {len(secret)} letters")
    print(GALLOWS[0])
    while wrong < MAX_WRONG and not letters <= guessed:
        print(show_word(secret, guessed))
        guess = read_guess(guessed)
        guessed.add(guess)
        if guess in letters:
            print(f"Yes, {guess!r} is in the word.")
        else:
            wrong += 1
            print(f"No {guess!r}. Guesses left:", MAX_WRONG - wrong)
            print(GALLOWS[wrong])
    won = letters <= guessed
    print(f"You {'won' if won else 'lost'}! The word was {secret!r}.")
    return won

# %% Step 5: One game
play(category, secret)

# %% Step 6: Several rounds and a score
def main():
    score = {"won": 0, "lost": 0}
    while True:
        category, secret = choose_word()
        if play(category, secret):
            score["won"] += 1
        else:
            score["lost"] += 1
        print(f"Score: {score['won']} won, {score['lost']} lost")
        if input("Play again? (y/n) ").strip().lower() != "y":
            break
    print("Thanks for playing!")

# %% Step 6: Several rounds and a score
random.seed(11)
main()
