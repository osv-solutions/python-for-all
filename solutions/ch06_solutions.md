# Solutions: Chapter 6, Lists and Tuples

Worked solutions to the exercises at the end of Chapter 6 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch06_solutions.ipynb`](ch06_solutions.ipynb) or the script `ch06_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 6.1

*Start with `nums = [5, 3, 8, 1]`. Append 10, insert 0 at the front, remove 8, and print the list, its length, its sum and its largest item after each step.*

```python
nums = [5, 3, 8, 1]
nums.append(10)
print(nums, len(nums), sum(nums), max(nums))
nums.insert(0, 0)
print(nums, len(nums), sum(nums), max(nums))
nums.remove(8)
print(nums, len(nums), sum(nums), max(nums))
```

Output:

```text
[5, 3, 8, 1, 10] 5 27 10
[0, 5, 3, 8, 1, 10] 6 27 10
[0, 5, 3, 1, 10] 5 19 10
```

`append` adds 10 at the end, `insert(0, 0)` puts the value 0 at index 0, and `remove(8)` deletes the first item equal to 8. Inserting 0 changes the length but not the sum; removing 8 lowers the sum from 27 to 19, while the largest item stays 10.

## Exercise 6.2

*Print `["kiwi", "Banana", "apple", "cherry"]` sorted alphabetically ignoring case, then by length, then in reverse alphabetical order.*

```python
words = ["kiwi", "Banana", "apple", "cherry"]
print(sorted(words, key=str.lower))
print(sorted(words, key=len))
print(sorted(words, key=str.lower, reverse=True))
```

Output:

```text
['apple', 'Banana', 'cherry', 'kiwi']
['kiwi', 'apple', 'Banana', 'cherry']
['kiwi', 'cherry', 'Banana', 'apple']
```

`key=str.lower` compares the lowercase versions, so `Banana` sorts between `apple` and `cherry` instead of first. `key=len` sorts by length; `Banana` and `cherry` both have six letters, and because sorting is stable they keep their original order. `reverse=True` combined with the same key gives reverse alphabetical order.

## Exercise 6.3

*Ask for numbers separated by spaces and print the smallest, the largest, the average and the numbers above the average.*

```python
numbers = []
for part in input("Numbers: ").split():
    numbers.append(float(part))
average = sum(numbers) / len(numbers)
above = []
for n in numbers:
    if n > average:
        above.append(n)
print(f"min {min(numbers)}, max {max(numbers)}, average {average:.2f}")
print("Above average:", above)
```

Output:

```text
Numbers: 4 8 15 16 23 42
min 4.0, max 42.0, average 18.00
Above average: [23.0, 42.0]
```

`split()` breaks the line into pieces at the spaces, and each piece is converted with `float`, so decimals are accepted as well. The average of the six numbers is 18.0, and two of them, 23 and 42, are above it.

## Exercise 6.4

*Remove duplicates from a list, keeping the first occurrence of each item in its original order.*

```python
items = [3, 1, 3, 2, 1]
unique = []
for item in items:
    if item not in unique:
        unique.append(item)
print(unique)
```

Output:

```text
[3, 1, 2]
```

Each item is appended only the first time it is seen. The result keeps the order of first appearance, `[3, 1, 2]`. Chapter 7 shows a set, which removes duplicates in one step but forgets the order; for long lists, checking membership in a set is also much faster than in a list.

## Exercise 6.5

*Use `zip` to combine days and sales into a small table, and print the day with the highest sales.*

```python
days = ["Mon", "Tue", "Wed"]
sales = [12.5, 15.0, 9.75]
for day, amount in zip(days, sales):
    print(f"{day}  ${amount:>6.2f}")
best = max(sales)
print("Best day:", days[sales.index(best)], f"(${best:.2f})")
```

Output:

```text
Mon  $ 12.50
Tue  $ 15.00
Wed  $  9.75
Best day: Tue ($15.00)
```

`zip` pairs each day with its sales. To find the best day, `max` finds the highest amount and `index` finds its position, which is also the position of the matching day in `days`. Tuesday sold the most.

## Exercise 6.6

*Explain why `changed = original` followed by `changed.append(4)` changes both, and fix it.*

`changed = original` doesn't copy the list; it gives the same list a second name, so appending through either name changes the one list that both refer to. Copy the list instead:

```python
original = [1, 2, 3]
changed = original.copy()
changed.append(4)
print(original, changed)
```

Output:

```text
[1, 2, 3] [1, 2, 3, 4]
```

Now `changed` is a separate list, and `original` stays `[1, 2, 3]`. `original[:]` or `list(original)` would work as well.

## Exercise 6.7

*Check a 3 × 3 tic-tac-toe board for three in a line.*

```python
board = [["X", "O", "X"],
         ["O", "X", "O"],
         ["O", "O", "X"]]
lines = []
for i in range(3):
    lines.append(board[i])                              # row i
    lines.append([board[0][i], board[1][i], board[2][i]])  # column i
lines.append([board[0][0], board[1][1], board[2][2]])
lines.append([board[0][2], board[1][1], board[2][0]])
winner = None
for line in lines:
    if line[0] != " " and line[0] == line[1] == line[2]:
        winner = line[0]
print("Winner:", winner)
```

Output:

```text
Winner: X
```

The program first collects all eight possible lines as lists of three cells: three rows, three columns (built from the same column index in each row) and the two diagonals. A line is a win when its first cell isn't empty and all three cells are equal, which a chained comparison checks in one go. Here X has the diagonal from the top left to the bottom right. With no winner, `winner` stays `None`.
