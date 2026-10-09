# Solutions: Chapter 14, Comprehensions, Iterators and Generators

Worked solutions to the exercises at the end of Chapter 14 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch14_solutions.ipynb`](ch14_solutions.ipynb) or the script `ch14_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 14.1

*Use comprehensions to build the cubes of 1 to 10, the long words of a sentence, a dictionary of squares and the set of vowels in a word.*

```python
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
```

Output:

```text
[1, 8, 27, 64, 125, 216, 343, 512, 729, 1000]
['Python', 'makes', 'everyday', 'tasks', 'quick', 'pleasant']
{1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
['a', 'i', 'o']
```

The first comprehension transforms every number, while the second has an `if` at the end and so only filters: of the seven words, only `and` has four letters or fewer and is left out. Curly braces with a colon give the dictionary, and curly braces without one give the set. *programming* contains the vowels `o`, `a` and `i`, and the set keeps each of them only once. A set has no order of its own, so the last line prints it through `sorted` to get the same output every time.

## Exercise 14.2

*Use `any` and `all` to check a list of numbers for a negative number, and a list of words for capital initials.*

```python
numbers = [12, 7, -3, 25, 0]
print("Any negative?", any(n < 0 for n in numbers))
cities = ["Paris", "Rome", "lisbon", "Oslo"]
print("All capitalized?", all(w[0].isupper() for w in cities))
cities[2] = "Lisbon"
print("All capitalized?", all(w[0].isupper() for w in cities))
```

Output:

```text
Any negative? True
All capitalized? False
All capitalized? True
```

Each question is a generator expression of `True` and `False` values passed straight to `any` or `all`. `any` stops at `-3`, the first negative number, and answers `True`. The first `all` stops at `lisbon` and answers `False`; once the name is corrected, every word passes and the answer is `True`. Without these two functions, each check would need a loop, a flag variable and a `break`.

## Exercise 14.3

*Rewrite three loops from earlier chapters as comprehensions or with `Counter`, and check that the results are the same.*

The first loop is the filter from Chapter 6, which keeps the passing scores:

```python
scores = [88, 52, 92, 67, 45, 79]
passed = []
for s in scores:
    if s >= 60:
        passed.append(s)
passed_2 = [s for s in scores if s >= 60]
print(passed)
print(passed_2, passed == passed_2)
```

Output:

```text
[88, 92, 67, 79]
[88, 92, 67, 79] True
```

Both versions keep the same four scores, and `==` confirms that the two lists are equal. The comprehension says in one line what the loop says in four: start empty, go through the scores, keep those of 60 or more.

The second loop comes from the grade book at the end of Chapter 6, which collects the scores out of a list of `(name, score)` tuples:

```python
results = [("Asha", 88), ("Ben", 52), ("Chen", 92),
           ("Dina", 67), ("Eli", 92), ("Femi", 79)]
scores = []
for name, score in results:
    scores.append(score)
scores_2 = [score for name, score in results]
print(scores_2, scores == scores_2)
print(f"average {sum(scores_2) / len(scores_2):.1f}")
```

Output:

```text
[88, 52, 92, 67, 92, 79] True
average 78.3
```

The `for` part of a comprehension can unpack tuples exactly like the loop header, so `name, score` works in both. The average is 78.3, as in Chapter 6. When the scores are needed only for the average, a generator expression, `sum(score for name, score in results)`, would not even build the list.

The third loop is the vote counting of Chapter 7:

```python
from collections import Counter

votes = ["tea", "coffee", "tea", "juice", "coffee", "tea"]
counts = {}
for vote in votes:
    counts[vote] = counts.get(vote, 0) + 1
counts_2 = Counter(votes)
print(counts)
print(counts_2)
print(counts == counts_2)
```

Output:

```text
{'tea': 3, 'coffee': 2, 'juice': 1}
Counter({'tea': 3, 'coffee': 2, 'juice': 1})
True
```

The `Counter` holds the same three counts: tea 3, coffee 2 and juice 1. It prints differently, with its own name and the most common item first, but a `Counter` is a dictionary, so comparing it with the hand-made one gives `True`. Counting is the place where `Counter` saves the most code.

## Exercise 14.4

*Write generators `evens(limit)` and `squares(numbers)`, chain them, and print the sum of the squares of the even numbers up to 100.*

```python
def evens(limit):
    for n in range(2, limit + 1, 2):
        yield n

def squares(numbers):
    for n in numbers:
        yield n * n

print(list(squares(evens(10))))
print(sum(squares(evens(100))))
```

Output:

```text
[4, 16, 36, 64, 100]
171700
```

`range(2, limit + 1, 2)` starts at 2 and steps by 2, and the `+ 1` makes "up to a limit" include the limit itself. `squares` doesn't care where its numbers come from: any iterable works, including another generator. The first line checks the pipeline on a small case, the squares of 2, 4, 6, 8 and 10. The second feeds the fifty even numbers up to 100 through the same pipeline into `sum`, which gives 171,700; at no point is a list of numbers stored.

## Exercise 14.5

*Write a generator `read_csv_rows(path)` that yields each row of a CSV file as a dictionary, and use it with `Counter` to count the expenses per category in `expenses.csv`.*

First, the sample file from Step 1 of Project 5, so that this solution has data to read:

```python
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
```

This block prints nothing; it just writes the ten sample expenses to the file. Now the generator and the count:

```python
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
```

Output:

```text
food       4
housing    2
transport  2
fun        2
total     10
```

`read_csv_rows` keeps the file open only while the rows are being read: the `with` block ends when the generator has yielded its last row. The generator expression passes just the category of each row to the `Counter`, so food comes first with 4 expenses, followed by housing, transport and fun with 2 each, in the order they first appear in the file. `total()` adds up all the counts, 10. The taxi with the amount `twenty` is counted too, because counting never looks at the amount; a report that adds up amounts would need the validation of Project 5.

## Exercise 14.6

*Use `itertools.combinations` to find all pairs of numbers in `[3, 8, 12, 5, 7, 10]` that add up to 15.*

```python
from itertools import combinations

numbers = [3, 8, 12, 5, 7, 10]
all_pairs = list(combinations(numbers, 2))
pairs = [(a, b) for a, b in all_pairs if a + b == 15]
print(len(all_pairs), "pairs checked")
print(pairs)
```

Output:

```text
15 pairs checked
[(3, 12), (8, 7), (5, 10)]
```

`combinations(numbers, 2)` yields every way to choose two different items, each pair only once and with the items in their original order: 15 pairs for six numbers. The comprehension unpacks each pair and keeps those that add up to 15: 3 and 12, 8 and 7, 5 and 10. Without `combinations`, this needs two nested loops, with the inner one starting just after the outer one's position so that no pair is counted twice.

## Exercise 14.7

*Write an iterable class `Deck` of 52 cards that supports `len()` and has a `deal(n)` method that deals from a shuffled copy.*

```python
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
```

Each card is a rank followed by the first letter of its suit: spades, hearts, diamonds or clubs. The cards are built with a comprehension with two `for` parts: for each suit, every rank, so `AS` (the ace of spades) comes first and `KC` (the king of clubs) last. `__iter__` must return an iterator, and the simplest one here is the list's own, from `iter` (a generator, as for the `Playlist` of the chapter, works too). `__len__` lets `len()` work. In `deal`, `random.sample` (Chapter 9) with the full length of the list returns a shuffled copy, and the slice keeps its first `n` cards; the deck itself always stays in order. Let's try it:

```python
deck = Deck()
print(len(deck), "cards")
print(list(deck)[:5], "...", list(deck)[-1])
print(sum(1 for card in deck if card.endswith("H")), "hearts")
random.seed(1)
print(deck.deal(5))
print(list(deck)[:5])
```

Output:

```text
52 cards
['AS', '2S', '3S', '4S', '5S'] ... KC
13 hearts
['9S', 'JD', '10C', '5S', '4H']
['AS', '2S', '3S', '4S', '5S']
```

The deck has 52 cards and can be used anywhere an iterable can: with `list`, slicing the result, and in a generator expression that counts the 13 hearts. `random.seed(1)` is called before dealing, so the program deals the same five cards on every run; it belongs in the program rather than in `deal`, because a real card game wants a different hand each time. The last line shows that the deck is still in its original order after the deal.
