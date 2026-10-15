# Solutions: Chapter 1, Welcome to Python

Worked solutions to the exercises at the end of Chapter 1 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch01_solutions.ipynb`](ch01_solutions.ipynb) or the script `ch01_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 1.1

*In the interactive shell, work out how many minutes there are in a week, and how many seconds there are in a day.*

A week has 7 days of 24 hours of 60 minutes, and a day has 24 hours of 60 minutes of 60 seconds. In the shell you would type each calculation after the `>>>` prompt; in a script, `print` shows the results:

```python
print(7 * 24 * 60)
print(24 * 60 * 60)
```

Output:

```text
10080
86400
```

There are 10,080 minutes in a week and 86,400 seconds in a day. Writing the calculation as `7 * 24 * 60`, rather than typing the answer, shows where the number comes from, which helps anyone reading the code (including you, later).

## Exercise 1.2

*Write a script `about_me.py` that prints your name, your city and your favorite food, each on its own line, followed by an empty line and a closing message.*

**File:** `about_me.py`

```python
print("Name: Vamsi")
print("City: Visakhapatnam")
print("Favorite food: mango pickle")
print()
print("Thanks for reading!")
```

Output:

```text
Name: Vamsi
City: Visakhapatnam
Favorite food: mango pickle

Thanks for reading!
```

Each `print` call writes one line, and `print()` with no arguments writes the empty line. Your own details will differ, of course.

## Exercise 1.3

*Use a single `print` call with `sep` to print the date `2026-10-08` from the three numbers 2026, 10 and 8.*

```python
print(2026, "10", "08", sep="-")
```

Output:

```text
2026-10-08
```

`print` puts the separator between the values instead of a space. The month and day are written as strings so that the leading zero is kept: the number `08` is not even valid Python, because whole numbers may not start with a zero.

## Exercise 1.4

*Each of these lines contains one mistake. Predict the kind of error, then run each one and fix it.*

The first line is missing its closing quote, so it is a syntax error:

```python
print("Python is fun)
```

Output:

```text
  File "C:\Users\ada\Documents\python-for-all\errors.py", line 1
    print("Python is fun)
          ^
SyntaxError: unterminated string literal (detected at line 1)
```

The fix is to add the quote: `print("Python is fun")`. The second line, `print("Python", "is" "fun")`, is missing a comma, but it is *not* an error:

```python
print("Python", "is" "fun")
```

Output:

```text
Python isfun
```

Python joins two strings written next to each other into one, so `"is" "fun"` becomes `"isfun"` and `print` receives only two values. The program runs but prints the wrong text, which is the hardest kind of bug to notice. Adding the comma fixes it. The third line misspells `print`, which is a runtime error:

```python
pritn("Python is fun")
```

Output:

```text
Traceback (most recent call last):
  File "C:\Users\ada\Documents\python-for-all\errors.py", line 1, in <module>
    pritn("Python is fun")
    ^^^^^
NameError: name 'pritn' is not defined. Did you mean: 'print'?
```

The `NameError` even suggests the right name. The last line has an extra closing parenthesis:

```python
print("Python is fun"))
```

Output:

```text
  File "C:\Users\ada\Documents\python-for-all\errors.py", line 1
    print("Python is fun"))
                          ^
SyntaxError: unmatched ')'
```

Python reports an "unmatched" parenthesis and points at it; deleting it fixes the line.

## Exercise 1.5

*Use `end` so that two `print` calls produce the single line `Ready, set, go!`.*

```python
print("Ready, set,", end=" ")
print("go!")
```

Output:

```text
Ready, set, go!
```

The first call ends with a space instead of a new line, so the second call continues on the same line.

## Exercise 1.6

*Write a program that prints a picture made of keyboard characters, at least five lines tall. Then introduce three different mistakes, one at a time, and write down the last line of each error message.*

Here is a small rocket:

```python
print("    /\\")
print("   /  \\")
print("  | () |")
print("  |    |")
print(" /|____|\\")
print("   /||\\")
```

Output:

```text
    /\
   /  \
  | () |
  |    |
 /|____|\
   /||\
```

Notice the doubled backslashes: a single backslash in a string starts an escape sequence (Chapter 3), so `\\` is needed to print one backslash. Typical mistakes and the last lines of their messages:

- Delete a closing quote: `SyntaxError: unterminated string literal (detected at line 1)`.

- Delete a closing parenthesis: `SyntaxError: '(' was never closed`.

- Type `Print` instead of `print`: `NameError: name 'Print' is not defined. Did you mean: 'print'?`

A fourth one is worth trying: delete one of a pair of backslashes at the end of a line, as in `print("    /\")`. The backslash then "escapes" the closing quote, which no longer ends the string, so Python reports an unterminated string.
