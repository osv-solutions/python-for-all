# Solutions: Chapter 2, Values, Variables and Types

Worked solutions to the exercises at the end of Chapter 2 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch02_solutions.ipynb`](ch02_solutions.ipynb) or the script `ch02_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 2.1

*Predict the result and the type of each expression, then check in the shell.*

```python
print(9 / 3, type(9 / 3))
print(9 // 2, type(9 // 2))
print(9 % 4, type(9 % 4))
print(2 ** 0.5, type(2 ** 0.5))
print("9" * 3, type("9" * 3))
print(int("9") * 3, type(int("9") * 3))
```

Output:

```text
3.0 <class 'float'>
4 <class 'int'>
1 <class 'int'>
1.4142135623730951 <class 'float'>
999 <class 'str'>
27 <class 'int'>
```

`9 / 3` is the float `3.0`, because `/` always gives a float. `9 // 2` is 4, the whole part of 4.5, and `9 % 4` is the remainder 1. Raising to the power 0.5 is the same as taking the square root, so `2 ** 0.5` is about 1.414. `"9" * 3` repeats the string, giving `"999"`, while `int("9") * 3` converts first and multiplies, giving the number 27.

## Exercise 2.2

*A recipe needs 250 grams of flour per batch. Store the number of batches in a variable and print the total amount of flour in kilograms.*

```python
grams_per_batch = 250
batches = 6
total_kg = batches * grams_per_batch / 1000
print(f"{batches} batches need {total_kg} kg of flour.")
```

Output:

```text
6 batches need 1.5 kg of flour.
```

Storing the 250 grams in a well-named variable, rather than writing the number into the calculation, makes the code explain itself. Dividing by 1000 converts grams to kilograms: six batches need 1.5 kg.

## Exercise 2.3

*Ask for a temperature in degrees Celsius and print it in Fahrenheit. Test it with 100 and with −40.*

```python
celsius = float(input("Temperature in °C: "))
fahrenheit = celsius * 9 / 5 + 32
print(f"{celsius} °C is {fahrenheit} °F")
```

Output:

```text
Temperature in °C: 100
100.0 °C is 212.0 °F
```

The input is converted with `float`, so temperatures such as 21.5 also work. 100 °C, the boiling point of water, is 212 °F. The second test:

```python
celsius = float(input("Temperature in °C: "))
fahrenheit = celsius * 9 / 5 + 32
print(f"{celsius} °C is {fahrenheit} °F")
```

Output:

```text
Temperature in °C: -40
-40.0 °C is -40.0 °F
```

−40 is the one temperature that is the same on both scales. Testing with values whose answers you already know is a quick way to catch a mistake in a formula.

## Exercise 2.4

*Ask the user for a number of seconds and print it as hours, minutes and seconds.*

```python
total = int(input("Number of seconds: "))
hours = total // 3600
minutes = total % 3600 // 60
seconds = total % 60
print(f"{hours} h {minutes} min {seconds} s")
```

Output:

```text
Number of seconds: 4000
1 h 6 min 40 s
```

An hour has 3,600 seconds, so `total // 3600` is the number of whole hours. `total % 3600` is what is left after the whole hours, 400 seconds here, and dividing that by 60 gives 6 whole minutes. Finally `total % 60` gives the 40 leftover seconds. Python evaluates `total % 3600 // 60` from left to right, because `%` and `//` have the same priority.

## Exercise 2.5

*Swap the values of `a = 5` and `b = 8`, first with a third variable, then with `a, b = b, a`.*

```python
a = 5
b = 8
temp = a
a = b
b = temp
print(a, b)
a, b = b, a
print(a, b)
```

Output:

```text
8 5
5 8
```

With a third variable, `temp` keeps a copy of the original `a` before `a` is overwritten. The one-line version swaps the values back: Python evaluates the whole right-hand side first (8 and 5, at that point) and only then assigns them to the names on the left, so no temporary variable is needed.

## Exercise 2.6

*Round each person's share up to the next whole dollar, and print how much extra tip that adds in total.*

```python
bill = float(input("Bill amount: $"))
tip_percent = int(input("Tip (%): "))
people = int(input("Number of people: "))
total = bill * (1 + tip_percent / 100)
share = total / people
rounded = -(-share // 1)
extra = rounded * people - total
print(f"Exact share: ${share:.2f}, rounded up: ${rounded:.2f}")
print(f"Extra tip in total: ${extra:.2f}")
```

Output:

```text
Bill amount: $84.60
Tip (%): 18
Number of people: 3
Exact share: $33.28, rounded up: $34.00
Extra tip in total: $2.17
```

The exact share is $33.276, which rounds up to $34. Here is why the hint works for `share = 33.276`: `-share` is −33.276, and floor division by 1 rounds *down*, toward minus infinity, giving −34.0. Negating that gives 34.0, which is 33.276 rounded *up*. When everyone pays $34, the group pays 3 × 34 = 102 dollars, $2.17 more than the exact total of $99.83, and that extra goes to the tip. Chapter 9 shows `math.ceil`, which rounds up directly.
