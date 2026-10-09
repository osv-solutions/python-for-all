# Solutions: Chapter 3, Working with Text

Worked solutions to the exercises at the end of Chapter 3 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch03_solutions.ipynb`](ch03_solutions.ipynb) or the script `ch03_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 3.1

*For `s = "programming"`, predict and then check the results.*

```python
s = "programming"
print(s[3], s[-2], s[3:7], s[:4])
print(s[::3], s.count("m"), s.find("g"), s.upper())
```

Output:

```text
g n gram prog
pgmn 2 3 PROGRAMMING
```

Counting from zero, `s[3]` is the fourth letter, `g`, and `s[-2]` is the second to last, `n`. The slice `s[3:7]` takes indexes 3 to 6, `gram`, and `s[:4]` takes the first four letters, `prog`. With a step of 3, `s[::3]` takes indexes 0, 3, 6 and 9: `p`, `g`, `a` and `i`. There are two `m`s, and the first `g` is at index 3.

## Exercise 3.2

*Print the number 1234.5 in five ways.*

```python
x = 1234.5
print(f"{x:.2f}")
print(f"{x:,.2f}")
print(f"[{x:>12}]")
print(f"{x:010.1f}")
print(f"{x / 10_000:.1%}")
```

Output:

```text
1234.50
1,234.50
[      1234.5]
00001234.5
12.3%
```

`.2f` gives two decimals, and adding a comma gives thousands separators as well. `>12` right-aligns the number in 12 characters; the square brackets make the padding visible. In `010.1f` the leading `0` pads with zeros up to a width of 10, counting the decimal point and the decimal. Finally, 1234.5 out of 10,000 is 0.12345, which the `%` format shows as `12.3%`.

## Exercise 3.3

*Ask for a sentence and print it with underscores for spaces, then print the number of words and the number of characters without spaces.*

```python
sentence = input("Sentence: ")
print(sentence.replace(" ", "_"))
print("Words:", len(sentence.split()))
print("Characters without spaces:", len(sentence.replace(" ", "")))
```

Output:

```text
Sentence: Python reads almost like English
Python_reads_almost_like_English
Words: 5
Characters without spaces: 28
```

`replace` swaps every space for an underscore. `split()` breaks the sentence into a list of words, and `len` counts them: five. Replacing every space with nothing, the empty string `""`, and measuring the result counts the other characters: 28.

## Exercise 3.4

*Ask for a date as `DD/MM/YYYY` and print it as `YYYY-MM-DD`.*

```python
text = input("Date (DD/MM/YYYY): ").strip()
day, month, year = text.split("/")
print(f"{year}-{month}-{day}")
print(f"{text[6:]}-{text[3:5]}-{text[:2]}")
```

Output:

```text
Date (DD/MM/YYYY): 08/10/2026
2026-10-08
2026-10-08
```

`split("/")` gives a list of three strings, and writing three names before `=` unpacks them into three variables in one step, just as `a, b = b, a` did in Chapter 2. The second version uses slicing instead: the year starts at index 6, the month occupies indexes 3 and 4, and the day indexes 0 and 1. Both print `2026-10-08`. The `split` version is easier to read and also copes with dates such as `8/10/2026`, where the positions shift.

## Exercise 3.5

*Ask for a word and print `True` if it is a palindrome, ignoring capital letters.*

```python
word = input("Word: ").strip().lower()
print(word == word[::-1])
```

Output:

```text
Word: Racecar
True
```

Converting to lowercase first makes `Racecar` and `racecar` the same, and `[::-1]` reverses the word. A palindrome is equal to its own reverse, so the comparison gives `True`.

## Exercise 3.6

*Extend the receipt with a 6% sales tax line and a grand total, keeping all the columns aligned.*

```python
subtotal = 2 * 3.5 + 1 * 2.25 + 3 * 4.0
tax = subtotal * 0.06
print(f"{'Item':<12}{'Qty':>5}{'Price':>10}")
print("-" * 27)
print(f"{'Coffee':<12}{2:>5}{3.5:>10.2f}")
print(f"{'Bagel':<12}{1:>5}{2.25:>10.2f}")
print(f"{'Orange juice':<12}{3:>5}{4.0:>10.2f}")
print("-" * 27)
print(f"{'Subtotal':<12}{subtotal:>15.2f}")
print(f"{'Tax (6%)':<12}{tax:>15.2f}")
print(f"{'Total':<12}{subtotal + tax:>15.2f}")
```

Output:

```text
Item          Qty     Price
---------------------------
Coffee          2      3.50
Bagel           1      2.25
Orange juice    3      4.00
---------------------------
Subtotal              21.25
Tax (6%)               1.27
Total                 22.52
```

The new lines use the same widths as the total line, 12 characters for the label and 15 for the amount, so all amounts end in the same column. Look closely at the amounts: 6% of $21.25 is exactly $1.275, but the receipt shows $1.27, and the total of $22.525 shows as $22.52. In binary, 1.275 is stored as a number very slightly below 1.275, so it rounds down. Real point-of-sale systems use the `decimal` module (mentioned in Chapter 2) to round money exactly as the tax rules require.

## Exercise 3.7

*Print the initials of a three-word name with dots, then the name as "Last, First Middle"; then make the second part work for any number of words.*

```python
parts = input("Full name: ").strip().title().split()
initials = parts[0][0] + "." + parts[1][0] + "." + parts[2][0] + "."
print(initials)
print(parts[2] + ", " + parts[0] + " " + parts[1])
print(parts[-1] + ", " + " ".join(parts[:-1]))
```

Output:

```text
Full name: mary ann evans
M.A.E.
Evans, Mary Ann
Evans, Mary Ann
```

`title` capitalizes each word, and `split` breaks the name into a list of three words. `parts[0][0]` takes the first word, then its first character. The last line works for any number of words: `parts[-1]` is always the last word, and `parts[:-1]` is a list of all the words before it, which `join` glues back together with spaces. Chapter 5's loops make it possible to build the initials for any number of words too: try it once you have read that chapter.
