"""Solutions to the Chapter 14 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch14_solutions.py

The explanations are in ch14_solutions.md."""

# %% Exercise 14.1
cubes = [n ** 3 for n in range(1, 11)]
sentence = "Python makes everyday tasks quick and pleasant"
long_words = [w for w in sentence.split() if len(w) > 4]
squares = {n: n * n for n in range(1, 6)}
word = "programming"
vowels = {ch for ch in word if ch in "aeiou"}
print(cubes)
print(long_words)
print(squares)
print(sorted(vowels))

# %% Exercise 14.2
numbers = [12, 7, -3, 25, 0]
print("Any negative?", any(n < 0 for n in numbers))
cities = ["Paris", "Rome", "lisbon", "Oslo"]
print("All capitalized?", all(w[0].isupper() for w in cities))
cities[2] = "Lisbon"
print("All capitalized?", all(w[0].isupper() for w in cities))

# %% Exercise 14.3
scores = [88, 52, 92, 67, 45, 79]
passed = []
for s in scores:
    if s >= 60:
        passed.append(s)
passed_2 = [s for s in scores if s >= 60]
print(passed)
print(passed_2, passed == passed_2)

# %% Exercise 14.3
results = [("Asha", 88), ("Ben", 52), ("Chen", 92),
           ("Dina", 67), ("Eli", 92), ("Femi", 79)]
scores = []
for name, score in results:
    scores.append(score)
scores_2 = [score for name, score in results]
print(scores_2, scores == scores_2)
print(f"average {sum(scores_2) / len(scores_2):.1f}")

# %% Exercise 14.3
from collections import Counter

votes = ["tea", "coffee", "tea", "juice", "coffee", "tea"]
counts = {}
for vote in votes:
    counts[vote] = counts.get(vote, 0) + 1
counts_2 = Counter(votes)
print(counts)
print(counts_2)
print(counts == counts_2)

# %% Exercise 14.4
def evens(limit):
    for n in range(2, limit + 1, 2):
        yield n

def squares(numbers):
    for n in numbers:
        yield n * n

print(list(squares(evens(10))))
print(sum(squares(evens(100))))

# %% Exercise 14.5
sample = """date,category,description,amount
2026-09-01,housing,September rent,1200.00
2026-09-03,food,Groceries,86.40
2026-09-09,transport,Bus pass,55.00
2026-09-14,fun,Concert tickets,90.00
2026-09-20,food,Groceries,74.25
2026-09-25,food,Dinner out,48.10
2026-10-01,housing,October rent,1200.00
2026-10-02,food,Groceries,92.30
2026-10-05,transport,Taxi,twenty
2026-10-06,fun,Cinema,24.00
"""
with open("expenses.csv", "w", encoding="utf-8") as f:
    f.write(sample)

# %% Exercise 14.5
import csv
from collections import Counter

def read_csv_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            yield row

rows = read_csv_rows("expenses.csv")
counts = Counter(row["category"] for row in rows)
for category, count in counts.most_common():
    print(f"{category:<10}{count:>2}")
print(f"{'total':<10}{counts.total():>2}")

# %% Exercise 14.6
from itertools import combinations

numbers = [3, 8, 12, 5, 7, 10]
all_pairs = list(combinations(numbers, 2))
pairs = [(a, b) for a, b in all_pairs if a + b == 15]
print(len(all_pairs), "pairs checked")
print(pairs)

# %% Exercise 14.7
import random

class Deck:
    RANKS = "A 2 3 4 5 6 7 8 9 10 J Q K".split()

    def __init__(self):
        self.cards = [r + s for s in "SHDC" for r in self.RANKS]

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    def deal(self, n):
        return random.sample(self.cards, len(self.cards))[:n]

# %% Exercise 14.7
deck = Deck()
print(len(deck), "cards")
print(list(deck)[:5], "...", list(deck)[-1])
print(sum(1 for card in deck if card.endswith("H")), "hearts")
random.seed(1)
print(deck.deal(5))
print(list(deck)[:5])
