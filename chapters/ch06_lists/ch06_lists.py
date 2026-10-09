"""Chapter 6: Lists and Tuples

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch06_lists.py

or open the notebook and run the cells in order.
"""

# %% 6.1 Creating lists
fruits = ["apple", "banana", "cherry"]
scores = [88, 92, 79, 95]
mixed = ["Ada", 36, True, None]
empty = []
print(fruits)
print(len(scores), len(empty), type(fruits))

# %% 6.1 Creating lists
print(list("hello"))
print(list(range(1, 6)))
print("red,green,blue".split(","))

# %% 6.2 Indexing and slicing
planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter"]
print(planets[0], planets[2], planets[-1])
print(planets[1:3])
print(planets[:2], planets[3:])
print(planets[::-1])

# %% 6.2 Indexing and slicing
print("Earth" in planets, "Pluto" in planets)
print(planets.index("Mars"))
print([3, 1, 3, 3, 2].count(3))

# %% 6.3 Lists can change
colors = ["red", "green", "blue"]
colors[1] = "yellow"
print(colors)
colors[-1] = colors[-1].upper()
print(colors)

# %% 6.3 Lists can change
tasks = ["email", "report"]
tasks.append("meeting")
tasks.insert(0, "coffee")
tasks.extend(["lunch", "call"])
print(tasks)

# %% 6.3 Lists can change
tasks.remove("report")
last = tasks.pop()
first = tasks.pop(0)
del tasks[1]
print(tasks, last, first)

# %% 6.4 Looping over lists
temperatures = [21.5, 24.0, 19.5, 26.5, 23.0]
for t in temperatures:
    print(f"{t:5.1f} °C")

# %% 6.4 Looping over lists
runners = ["Asha", "Ben", "Chen"]
for place, name in enumerate(runners, start=1):
    print(f"{place}. {name}")

# %% 6.4 Looping over lists
names = ["pen", "notebook", "stapler"]
prices = [1.25, 3.50, 7.99]
for name, price in zip(names, prices):
    print(f"{name:<10}${price:>6.2f}")

# %% 6.4 Looping over lists
scores = [88, 52, 92, 67, 45, 79]
passed = []
for s in scores:
    if s >= 60:
        passed.append(s)
print(passed)
print(len(passed), "of", len(scores), "passed")

# %% 6.5 Built-in functions for lists
scores = [88, 52, 92, 67, 45, 79]
print(len(scores), sum(scores), min(scores), max(scores))
print(f"average: {sum(scores) / len(scores):.1f}")
print(sorted(scores))
print(sorted(scores, reverse=True)[:3])

# %% 6.5 Built-in functions for lists
words = ["pear", "Fig", "apple", "banana"]
words.sort()
print(words)
words.sort(key=str.lower)
print(words)
result = words.sort()
print(result)

# %% 6.6 Two names, one list
a = [1, 2, 3]
b = a
b.append(4)
print("a:", a)
print("b:", b)
print(a is b)

# %% 6.6 Two names, one list
a = [1, 2, 3]
c = a.copy()
c.append(4)
print("a:", a)
print("c:", c)
print(a == c, a is c)

# %% 6.7 Lists inside lists
board = [["X", "O", "X"],
         ["O", "X", "O"],
         ["O", "X", "X"]]
print(board[0])
print(board[1][2])
for row in board:
    print(" | ".join(row))

# %% 6.8 Tuples
point = (3, 4)
rgb = (255, 128, 0)
print(point[0], rgb[-1], len(rgb))
print(type(point))

# %% 6.8 Tuples
# This example stops with an error on purpose (see the book).
try:
    point = (3, 4)
    point[0] = 10
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% 6.8 Tuples
size = 1920, 1080
print(size, type(size))
width, height = size
print(width, "by", height)
a, b = 5, 8
a, b = b, a
print(a, b)

# %% 6.8 Tuples
first, *middle, last = [10, 20, 30, 40, 50]
print(first, middle, last)

# %% 6.9 Putting it together: a grade book
results = [("Asha", 88), ("Ben", 52), ("Chen", 92),
           ("Dina", 67), ("Eli", 92), ("Femi", 79)]
scores = []
for name, score in results:
    scores.append(score)
average = sum(scores) / len(scores)
print(f"{len(results)} students, average {average:.1f}")

# %% 6.9 Putting it together: a grade book
ranking = []
for name, score in results:
    ranking.append((-score, name))
ranking.sort()
for place, (neg, name) in enumerate(ranking, start=1):
    note = "" if -neg >= 60 else "  below 60"
    print(f"{place}. {name:<5}{-neg:>4}{note}")
