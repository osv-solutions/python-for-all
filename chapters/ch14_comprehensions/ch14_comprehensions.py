"""Chapter 14: Comprehensions, Iterators and Generators

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch14_comprehensions.py

or open the notebook and run the cells in order.
"""

# %% 14.1 List comprehensions
squares = []
for n in range(1, 6):
    squares.append(n * n)
print(squares)

# %% 14.1 List comprehensions
squares = [n * n for n in range(1, 6)]
print(squares)

# %% 14.1 List comprehensions
scores = [88, 52, 92, 67, 45, 79]
passed = [s for s in scores if s >= 60]
curved = [min(s + 5, 100) for s in scores]
labels = ["pass" if s >= 60 else "fail" for s in scores]
print(passed)
print(curved)
print(labels)

# %% 14.1 List comprehensions
pairs = [(x, y) for x in range(1, 4) for y in "ab"]
print(pairs)
grid = [[1, 2, 3], [4, 5, 6]]
flat = [n for row in grid for n in row]
print(flat)

# %% 14.2 Dictionary and set comprehensions
words = ["apple", "fig", "banana", "kiwi", "fig"]
lengths = {w: len(w) for w in words}
initials = {w[0] for w in words}
prices = {"tea": 2.5, "cake": 3.75, "soup": 5.25}
discounted = {item: round(p * 0.9, 2) for item, p in prices.items()}
print(lengths)
print(sorted(initials))
print(discounted)

# %% 14.3 Generator expressions
print(sum(n * n for n in range(1, 101)))
words = ["Python", "is", "fun"]
print(max(len(w) for w in words))
print("-".join(w.upper() for w in words))

# %% 14.3 Generator expressions
import sys

as_list = [n for n in range(1_000_000)]
as_gen = (n for n in range(1_000_000))
print(sys.getsizeof(as_list), "bytes for the list")
print(sys.getsizeof(as_gen), "bytes for the generator")

# %% 14.3 Generator expressions
password = "Secret42!"
print(any(ch.isdigit() for ch in password))
print(any(ch.isupper() for ch in password))
print(all(ch.isalnum() for ch in password))
scores = [88, 92, 79]
print(all(s >= 60 for s in scores))

# %% 14.4 How for loops work: iterators
colors = ["red", "green", "blue"]
it = iter(colors)
print(next(it))
print(next(it))
print(next(it))

# %% 14.4 How for loops work: iterators
# This example stops with an error on purpose (see the book).
try:
    colors = ["red", "green", "blue"]
    it = iter(colors)
    for _ in range(4):
        print(next(it))
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% 14.5 Generators
def countdown(n):
    print("starting")
    while n > 0:
        yield n
        n -= 1
    print("done")

for value in countdown(3):
    print("got", value)

# %% 14.5 Generators
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

for n in fibonacci():
    if n > 100:
        break
    print(n, end=" ")
print()

# %% 14.5 Generators
from pathlib import Path

Path("readings.txt").write_text(
    "# sensor log\n12.5\n\n13.1\n# reset\n12.9\n", encoding="utf-8")

def lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.strip()

def values(lines):
    for line in lines:
        if line and not line.startswith("#"):
            yield float(line)

print(list(values(lines("readings.txt"))))

# %% 14.6 Tools for iterators: itertools
from itertools import islice, chain, combinations, accumulate

print(list(islice(fibonacci(), 10)))
print(list(chain([1, 2], (3, 4), "ab")))
print(list(combinations("ABC", 2)))
print(list(accumulate([3, 1, 4, 1, 5])))

# %% 14.7 Counting with collections.Counter
from collections import Counter

votes = ["tea", "coffee", "tea", "juice", "coffee", "tea"]
counts = Counter(votes)
print(counts)
print(counts["tea"], counts["water"])
print(counts.most_common(2))

# %% 14.8 Making your own classes iterable
class Playlist:
    def __init__(self, name, songs):
        self.name = name
        self.songs = list(songs)

    def __iter__(self):
        for song in self.songs:
            yield song

trip = Playlist("Road trip", ["Hey Jude", "Imagine", "Respect"])
for song in trip:
    print(song)
print([s.upper() for s in trip], "Imagine" in trip)

# %% 14.9 Putting it together: analyzing a log file
log = """2026-10-08 09:00:01 INFO  server started
2026-10-08 09:02:17 WARN  disk 81% full
2026-10-08 09:05:44 ERROR timeout talking to db
2026-10-08 09:05:45 INFO  retrying
2026-10-08 09:06:10 ERROR timeout talking to db
2026-10-08 09:12:00 ERROR payment service unavailable
2026-10-08 09:15:30 WARN  disk 85% full
"""
Path("app.log").write_text(log, encoding="utf-8")

# %% 14.9 Putting it together: analyzing a log file
def parse(lines):
    for line in lines:
        day, time, level, message = line.split(maxsplit=3)
        yield time, level, message

events = parse(lines("app.log"))
problems = [e for e in events if e[1] in ("WARN", "ERROR")]
for time, level, message in problems:
    print(f"{time}  {level:<6}{message}")

# %% 14.9 Putting it together: analyzing a log file
levels = Counter(level for _, level, _ in problems)
errors = Counter(m for _, lvl, m in problems if lvl == "ERROR")
print(dict(levels))
for message, count in errors.most_common():
    print(f"{count} x {message}")
