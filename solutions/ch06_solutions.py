"""Solutions to the Chapter 6 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch06_solutions.py

The explanations are in ch06_solutions.md."""

# %% Exercise 6.1
nums = [5, 3, 8, 1]
nums.append(10)
print(nums, len(nums), sum(nums), max(nums))
nums.insert(0, 0)
print(nums, len(nums), sum(nums), max(nums))
nums.remove(8)
print(nums, len(nums), sum(nums), max(nums))

# %% Exercise 6.2
words = ["kiwi", "Banana", "apple", "cherry"]
print(sorted(words, key=str.lower))
print(sorted(words, key=len))
print(sorted(words, key=str.lower, reverse=True))

# %% Exercise 6.3
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

# %% Exercise 6.4
items = [3, 1, 3, 2, 1]
unique = []
for item in items:
    if item not in unique:
        unique.append(item)
print(unique)

# %% Exercise 6.5
days = ["Mon", "Tue", "Wed"]
sales = [12.5, 15.0, 9.75]
for day, amount in zip(days, sales):
    print(f"{day}  ${amount:>6.2f}")
best = max(sales)
print("Best day:", days[sales.index(best)], f"(${best:.2f})")

# %% Exercise 6.6
original = [1, 2, 3]
changed = original.copy()
changed.append(4)
print(original, changed)

# %% Exercise 6.7
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
