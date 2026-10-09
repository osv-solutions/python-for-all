"""Solutions to the Chapter 8 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch08_solutions.py

The explanations are in ch08_solutions.md."""

# %% Exercise 8.1
def c_to_f(celsius):
    """Return the temperature in degrees Fahrenheit."""
    return celsius * 9 / 5 + 32

for c in range(-10, 41, 10):
    print(f"{c:>4} °C = {c_to_f(c):5.1f} °F")

# %% Exercise 8.2
def is_even(n):
    return n % 2 == 0

def count_even(numbers):
    count = 0
    for n in numbers:
        if is_even(n):
            count += 1
    return count

print(is_even(10), is_even(7))
print(count_even([3, 8, 12, 5, 6, 1]))

# %% Exercise 8.3
def initials(full_name):
    """Return the initials of a name, such as "M.A.E."."""
    result = ""
    for word in full_name.split():
        result += word[0].upper() + "."
    return result

print(initials("mary ann evans"))
print(initials("Guido van Rossum"))

# %% Exercise 8.4
def describe_list(numbers, decimals=1):
    mean = round(sum(numbers) / len(numbers), decimals)
    return (f"{len(numbers)} numbers, min {min(numbers)}, "
            f"max {max(numbers)}, mean {mean}")

print(describe_list([2, 9, 4, 7, 5, 5]))
print(describe_list([2, 9, 4, 7, 5, 5], decimals=3))

# %% Exercise 8.5
def make_receipt(*prices, tax_rate=0.06):
    subtotal = sum(prices)
    tax = round(subtotal * tax_rate, 2)
    return subtotal, tax, round(subtotal + tax, 2)

print(make_receipt(3.50, 2.25, 12.00))
sub, tax, total = make_receipt(3.50, 2.25, 12.00, tax_rate=0.0825)
print(f"subtotal {sub:.2f}, tax {tax:.2f}, total {total:.2f}")

# %% Exercise 8.6
def ask_float(prompt, low, high):
    """Ask until the user types a decimal number from low to high."""
    while True:
        text = input(prompt).strip()
        if text.replace(".", "", 1).isdigit():
            if low <= float(text) <= high:
                return float(text)
        print(f"  Please enter a number from {low} to {high}.")

bill = ask_float("Bill amount ($): ", 0.01, 10_000)
tip_percent = ask_float("Tip (%): ", 0, 100)
people = int(ask_float("Number of people: ", 1, 50))
share = bill * (1 + tip_percent / 100) / people
print(f"Each person pays ${share:.2f}")

# %% Exercise 8.7
import random

def choose_level():
    level = input("Difficulty (easy, normal, hard): ").strip().lower()
    match level:
        case "easy":
            return 20, 5
        case "hard":
            return 1000, 10
        case _:
            return 100, 7

# %% Exercise 8.7
def play(top, max_tries):
    secret = random.randint(1, top)
    for tries in range(1, max_tries + 1):
        text = input(f"Guess {tries} of {max_tries}: ").strip()
        guess = int(text) if text.isdigit() else 0
        if guess == secret:
            print(f"  Correct in {tries} tries!")
            return True
        print("  Too low." if guess < secret else "  Too high.")
    print(f"  Out of tries! It was {secret}.")
    return False

# %% Exercise 8.7
def main():
    games = wins = 0
    while True:
        top, max_tries = choose_level()
        games += 1
        if play(top, max_tries):
            wins += 1
        if input("Play again? (y/n) ").strip().lower() != "y":
            break
    print(f"You won {wins} of {games} games.")

random.seed(7)
main()
