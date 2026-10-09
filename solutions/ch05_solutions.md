# Solutions: Chapter 5, Repeating Work with Loops

Worked solutions to the exercises at the end of Chapter 5 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch05_solutions.ipynb`](ch05_solutions.ipynb) or the script `ch05_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 5.1

*Print the even numbers from 2 to 20 on one line, first with a `while` loop and then with a `for` loop and `range`.*

```python
n = 2
while n <= 20:
    print(n, end=" ")
    n += 2
print()
for n in range(2, 21, 2):
    print(n, end=" ")
print()
```

Output:

```text
2 4 6 8 10 12 14 16 18 20 
2 4 6 8 10 12 14 16 18 20
```

The `while` version needs three pieces: a starting value, a condition and an update. The `for` version packs all three into `range(2, 21, 2)`. The stop value is 21, so that 20 is included. Both print the same ten numbers.

## Exercise 5.2

*Ask for a word and print each of its letters on its own line, numbered from 1.*

```python
word = input("Word: ")
number = 1
for letter in word:
    print(f"{number}: {letter}")
    number += 1
```

Output:

```text
Word: loop
1: l
2: o
3: o
4: p
```

The counter `number` starts at 1 and goes up after each letter. (Chapter 6 shows `enumerate`, which does the counting for you.)

## Exercise 5.3

*Ask for a whole number n and print its factorial. What is the factorial of 20?*

```python
n = int(input("n: "))
factorial = 1
for k in range(2, n + 1):
    factorial *= k
print(f"{n}! = {factorial:,}")
```

Output:

```text
n: 20
20! = 2,432,902,008,176,640,000
```

The accumulator starts at 1, not 0, because it collects a product: starting at 0 would make everything 0. The loop multiplies by every number from 2 to *n*. The factorial of 20 is 2,432,902,008,176,640,000, about 2.4 quintillion, and Python's integers hold it exactly. The program also works for 0 and 1, whose factorial is 1, because the loop then doesn't run at all.

## Exercise 5.4

*Read test scores until a blank line, then print how many there were, their average, and the highest and lowest.*

```python
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
```

Output:

```text
Score (blank to finish): 72
Score (blank to finish): 88
Score (blank to finish): 95
Score (blank to finish): 61
Score (blank to finish): 
4 scores, average 79.0, highest 95.0, lowest 61.0
```

`highest = lowest = None` sets both variables to `None` in one line, meaning "no score seen yet". Each new score updates the counter and the total, and replaces the highest or lowest if it beats them. The final `if` protects against dividing by zero when the user enters nothing at all. For the four scores, the average is 316 / 4 = 79.0.

## Exercise 5.5

*Print the multiplication table from 1 to 10 with a header row and a header column.*

```python
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
```

Output:

```text
   |   1   2   3   4   5   6   7   8   9  10
---+----------------------------------------
 1 |   1   2   3   4   5   6   7   8   9  10
 2 |   2   4   6   8  10  12  14  16  18  20
 3 |   3   6   9  12  15  18  21  24  27  30
 4 |   4   8  12  16  20  24  28  32  36  40
 5 |   5  10  15  20  25  30  35  40  45  50
 6 |   6  12  18  24  30  36  42  48  54  60
 7 |   7  14  21  28  35  42  49  56  63  70
 8 |   8  16  24  32  40  48  56  64  72  80
 9 |   9  18  27  36  45  54  63  72  81  90
10 |  10  20  30  40  50  60  70  80  90 100
```

The header row prints the column numbers in the same 4-character fields as the products, after a 4-character corner (`"   |"`) that matches the row labels. The separator line is `---+` followed by 40 hyphens, one for each character of the ten columns. Each row starts with its number in 2 characters plus `" |"`, again 4 characters wide, so everything lines up.

## Exercise 5.6

*Simulate 1,000 rolls of two dice with `random.seed(1)` and count how often the total is 7.*

```python
import random

random.seed(1)
sevens = 0
for _ in range(1000):
    total = random.randint(1, 6) + random.randint(1, 6)
    if total == 7:
        sevens += 1
print(f"{sevens} sevens in 1,000 rolls ({sevens / 1000:.1%})")
print(f"expected about {1000 / 6:.0f} ({1 / 6:.1%})")
```

Output:

```text
168 sevens in 1,000 rolls (16.8%)
expected about 167 (16.7%)
```

Six of the 36 equally likely combinations of two dice add up to 7 (1+6, 2+5, 3+4, 4+3, 5+2, 6+1), so the expected share is one in six, about 16.7%. The simulation comes close; with more rolls it would come closer still. Change the seed, or remove it, and the count changes a little from run to run.

## Exercise 5.7

*FizzBuzz: print the numbers from 1 to 30, replacing multiples of 3, 5 and both.*

```python
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
```

Output:

```text
1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz 16 17 Fizz 19 Buzz Fizz 22 23 Fizz Buzz 26 Fizz 28 29 FizzBuzz
```

A number divisible by both 3 and 5 is divisible by 15, and that check must come first; otherwise the `n % 3 == 0` branch would catch 15 and 30 and print `Fizz`. To print the values separated by commas, with no comma after the last one, build a string and add the separator only between items:

```python
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
```

Output:

```text
1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14, FizzBuzz, 16, 17, Fizz, 19, Buzz, Fizz, 22, 23, Fizz, Buzz, 26, Fizz, 28, 29, FizzBuzz
```

`if line:` is false only for the very first item, when `line` is still empty, so the comma goes in front of every item except the first.
