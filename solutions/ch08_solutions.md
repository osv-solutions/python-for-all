# Solutions: Chapter 8, Functions

Worked solutions to the exercises at the end of Chapter 8 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch08_solutions.ipynb`](ch08_solutions.ipynb) or the script `ch08_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 8.1

*Write `c_to_f(celsius)` and use it to print a conversion table from −10 °C to 40 °C in steps of 10.*

```python
def c_to_f(celsius):
    """Return the temperature in degrees Fahrenheit."""
    return celsius * 9 / 5 + 32

for c in range(-10, 41, 10):
    print(f"{c:>4} °C = {c_to_f(c):5.1f} °F")
```

Output:

```text
 -10 °C =  14.0 °F
   0 °C =  32.0 °F
  10 °C =  50.0 °F
  20 °C =  68.0 °F
  30 °C =  86.0 °F
  40 °C = 104.0 °F
```

The function only calculates; the loop does the printing. `range(-10, 41, 10)` stops before 41, so 40 is the last value.

## Exercise 8.2

*Write `is_even(n)` and `count_even(numbers)`, which uses it.*

```python
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
```

Output:

```text
True False
3
```

`is_even` returns the result of the comparison directly; there is no need for `if ...: return True else: return False`. `count_even` reuses it, which keeps each function short and makes the loop read like a sentence. Three of the six numbers are even.

## Exercise 8.3

*Write `initials(full_name)` for a name of any length.*

```python
def initials(full_name):
    """Return the initials of a name, such as "M.A.E."."""
    result = ""
    for word in full_name.split():
        result += word[0].upper() + "."
    return result

print(initials("mary ann evans"))
print(initials("Guido van Rossum"))
```

Output:

```text
M.A.E.
G.V.R.
```

The loop that Chapter 3's exercise couldn't use yet handles any number of words. `word[0].upper()` capitalizes each initial, whatever the user typed.

## Exercise 8.4

*Write `describe_list(numbers, decimals=1)` that returns a summary string.*

```python
def describe_list(numbers, decimals=1):
    mean = round(sum(numbers) / len(numbers), decimals)
    return (f"{len(numbers)} numbers, min {min(numbers)}, "
            f"max {max(numbers)}, mean {mean}")

print(describe_list([2, 9, 4, 7, 5, 5]))
print(describe_list([2, 9, 4, 7, 5, 5], decimals=3))
```

Output:

```text
6 numbers, min 2, max 9, mean 5.3
6 numbers, min 2, max 9, mean 5.333
```

The mean of the six numbers is 5.333..., shown as 5.3 with the default of 1 decimal and as 5.333 when the caller passes `decimals=3`. The function *returns* the text rather than printing it, so the caller can print it, save it or put it in a report.

## Exercise 8.5

*Write `make_receipt(*prices, tax_rate=0.06)` that returns the subtotal, tax and total.*

```python
def make_receipt(*prices, tax_rate=0.06):
    subtotal = sum(prices)
    tax = round(subtotal * tax_rate, 2)
    return subtotal, tax, round(subtotal + tax, 2)

print(make_receipt(3.50, 2.25, 12.00))
sub, tax, total = make_receipt(3.50, 2.25, 12.00, tax_rate=0.0825)
print(f"subtotal {sub:.2f}, tax {tax:.2f}, total {total:.2f}")
```

Output:

```text
(17.75, 1.06, 18.81)
subtotal 17.75, tax 1.46, total 19.21
```

`*prices` collects any number of prices into a tuple. A parameter that comes *after* `*prices` can only be passed by keyword, which is exactly right for an option such as `tax_rate`: in `make_receipt(3.5, 2.25, 0.0825)`, the 0.0825 would simply be another price. The function returns three values as a tuple, which the second call unpacks.

## Exercise 8.6

*Write `ask_float(prompt, low, high)` and use it to let the tip calculator accept cents.*

```python
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
```

Output:

```text
Bill amount ($): 84.60
Tip (%): 18
Number of people: 3
Each person pays $33.28
```

Removing at most one decimal point with `replace(".", "", 1)` leaves only digits for valid numbers such as `84.60`, while `8.4.6` or `abc` fail. The check doesn't accept negative numbers, which is fine for prices; Chapter 10 shows a simpler way with `try` and `except`. The number of people is converted with `int`, though a smarter program would use `ask_int` from the chapter, so that `2.5` people is refused.

## Exercise 8.7

*Rewrite the number guessing game with `choose_level`, `play` and `main` functions.*

```python
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
```

`choose_level` returns the range and the number of tries as a tuple. Then the game itself, which returns `True` for a win:

```python
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
```

A `for` loop over the tries replaces the counter of the original version, and `return True` ends both the loop and the function as soon as the player wins. (For brevity, this version counts an invalid answer as a try; restoring the `continue` check of Project 1 is a good extra exercise.) Finally `main`, which plays until the player stops and counts the wins:

```python
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
```

Output:

```text
Difficulty (easy, normal, hard): easy
Guess 1 of 5: 10
  Too low.
Guess 2 of 5: 15
  Too high.
Guess 3 of 5: 12
  Too high.
Guess 4 of 5: 11
  Correct in 4 tries!
Play again? (y/n) y
Difficulty (easy, normal, hard): normal
Guess 1 of 7: 50
  Too high.
Guess 2 of 7: 40
  Too high.
Guess 3 of 7: 30
  Too high.
Guess 4 of 7: 25
  Too high.
Guess 5 of 7: 24
  Too high.
Guess 6 of 7: 23
  Too high.
Guess 7 of 7: 22
  Too high.
  Out of tries! It was 20.
Play again? (y/n) n
You won 1 of 2 games.
```

`games = wins = 0` sets both counters at once. Each function does one job, so `main` reads like a summary of the program. With the seed of Project 1, the easy game's secret is 11 again; the player won it in four tries and then lost the normal game, whose secret was 20.
