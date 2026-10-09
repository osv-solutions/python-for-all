# Solutions: Chapter 4, Making Decisions

Worked solutions to the exercises at the end of Chapter 4 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch04_solutions.ipynb`](ch04_solutions.ipynb) or the script `ch04_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 4.1

*Predict whether each condition is true or false, then check.*

```python
print(7 >= 7, "cat" < "dog", "Cat" == "cat")
print(not (3 > 2), 5 < 3 or 2 < 4, 1 <= 0.5 <= 2)
print(bool("0"))
```

Output:

```text
True True False
False True False
True
```

`7 >= 7` is true because the values are equal. `"cat" < "dog"` is true because `c` comes before `d`, but `"Cat" == "cat"` is false: capital letters matter. `3 > 2` is true, so `not` makes it false. In `5 < 3 or 2 < 4` the first comparison is false but the second is true, which is enough for `or`. The chained comparison `1 <= 0.5 <= 2` is false because 0.5 is less than 1. Finally, `"0"` is a non-empty string, so it is truthy, even though the number 0 would be falsy.

## Exercise 4.2

*Ask the user for a number and print whether it is positive, negative or zero.*

```python
number = float(input("A number: "))
if number > 0:
    print("positive")
elif number < 0:
    print("negative")
else:
    print("zero")
```

Output:

```text
A number: -3.5
negative
```

Using `float` accepts decimals as well as whole numbers. Exactly one of the three branches runs; for −3.5 it is the `elif`.

## Exercise 4.3

*Print whether a year is a leap year. Test with 2024, 1900, 2000 and 2026.*

```python
year = int(input("Year: "))
if year % 400 == 0:
    print(year, "is a leap year.")
elif year % 100 == 0:
    print(year, "is not a leap year.")
elif year % 4 == 0:
    print(year, "is a leap year.")
else:
    print(year, "is not a leap year.")
```

Output:

```text
Year: 1900
1900 is not a leap year.
```

The order of the branches does the work, as with the grades in the chapter. Years divisible by 400 are checked first, then the other century years, which are not leap years, and only then the ordinary rule of divisibility by 4. 1900 is divisible by 100 but not by 400, so it was not a leap year. The whole rule also fits in one Boolean expression, which makes the four tests quick:

```python
for year in (2024, 1900, 2000, 2026):
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    print(year, leap)
```

Output:

```text
2024 True
1900 False
2000 True
2026 False
```

(This uses a `for` loop from Chapter 5 to try four years in a row.) A year is a leap year if it is divisible by 4 and either not a century year or divisible by 400. The parentheses are essential, because `and` is applied before `or`. 2024 and 2000 are leap years; 1900 and 2026 are not.

## Exercise 4.4

*Write a body mass index calculator and print the category.*

```python
weight = float(input("Weight (kg): "))
height = float(input("Height (m): "))
bmi = weight / height ** 2
if bmi < 18.5:
    category = "underweight"
elif bmi < 25:
    category = "normal"
elif bmi < 30:
    category = "overweight"
else:
    category = "obese"
print(f"BMI {bmi:.1f}: {category}")
```

Output:

```text
Weight (kg): 70
Height (m): 1.75
BMI 22.9: normal
```

`height ** 2` is calculated before the division, because powers come first. A person of 70 kg and 1.75 m has a BMI of 22.9, which is in the normal range. Because each `elif` is reached only when the previous conditions were false, `bmi < 25` really means "from 18.5 up to 25".

## Exercise 4.5

*Ask for a new password and print what is wrong with it, if anything.*

```python
password = input("New password: ")
ok = True
if len(password) < 8:
    print("- It must have at least 8 characters.")
    ok = False
if password.lower() == password:
    print("- It must contain a capital letter.")
    ok = False
if "password" in password.lower():
    print('- It must not contain the word "password".')
    ok = False
if ok:
    print("Password accepted.")
```

Output:

```text
New password: mypassword1
- It must contain a capital letter.
- It must not contain the word "password".
```

This program uses three separate `if` statements rather than an `elif` chain, because a password can have several problems at once and the user should hear about all of them. The variable `ok` starts as `True` and is set to `False` by any failed check, so the final message appears only if every check passed. `mypassword1` is long enough but has no capital letter and contains the word "password". Converting to lowercase before the `in` test catches `PassWord` and `PASSWORD` too.

## Exercise 4.6

*Extend the ticket machine for Mondays and Sundays, and explain why `match` is a poor fit for the grade calculator.*

```python
age = int(input("Your age: "))
if age < 5:
    price = 0
elif age < 18 or age >= 65:
    price = 8
else:
    price = 15
day = input("Day of your visit: ").strip().lower()
match day:
    case "monday":
        print("Sorry, the museum is closed on Mondays.")
    case "tuesday":
        print(f"Ticket price: ${price / 2:.2f}")
    case "sunday":
        print(f"Ticket price: ${price + 2:.2f}")
    case _:
        print(f"Ticket price: ${price:.2f}")
```

Output:

```text
Your age: 30
Day of your visit: sunday
Ticket price: $17.00
```

Each case now prints its own message, so the Monday case can skip the price altogether. (For brevity, this version leaves out the input check from the chapter.) An adult visiting on a Sunday pays $15 + $2 = $17.

The grade calculator compares a score with *ranges* (90 and above, 80 and above, and so on), while `match` compares a value with fixed *patterns*. You would need a case for every possible score, or `case _ if score >= 90:` style conditions, called **guards**, which turn each case back into an `if`. Use `match` when one value is checked against a set of fixed options, such as commands, days or menu choices, and `if`/`elif` for ranges and combined conditions.

## Exercise 4.7

*Write a rock, paper, scissors referee.*

```python
p1 = input("Player 1 (rock, paper, scissors): ").strip().lower()
p2 = input("Player 2 (rock, paper, scissors): ").strip().lower()
valid = ("rock", "paper", "scissors")
if p1 not in valid or p2 not in valid:
    print("Both players must choose rock, paper or scissors.")
elif p1 == p2:
    print("A draw!")
elif (p1 == "rock" and p2 == "scissors"
      or p1 == "scissors" and p2 == "paper"
      or p1 == "paper" and p2 == "rock"):
    print("Player 1 wins!")
else:
    print("Player 2 wins!")
```

Output:

```text
Player 1 (rock, paper, scissors): Rock
Player 2 (rock, paper, scissors): scissors
Player 1 wins!
```

The first branch rules out invalid input, the second handles draws, and the third lists the three ways player 1 can win. After those, the only possibility left is that player 2 won, so the `else` needs no condition. The long condition is split over three lines inside parentheses, which Python allows, and each line is one complete winning pair; since `and` binds more tightly than `or`, no further parentheses are needed. Rock beats scissors, so player 1 wins.
