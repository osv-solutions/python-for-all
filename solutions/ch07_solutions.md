# Solutions: Chapter 7, Dictionaries and Sets

Worked solutions to the exercises at the end of Chapter 7 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch07_solutions.ipynb`](ch07_solutions.ipynb) or the script `ch07_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 7.1

*Ask for a country and print its capital, or a friendly message if the country isn't in the dictionary.*

```python
capitals = {"France": "Paris", "Japan": "Tokyo", "Kenya": "Nairobi",
            "Peru": "Lima", "India": "New Delhi"}
country = input("Country: ").strip().title()
capital = capitals.get(country)
if capital:
    print(f"The capital of {country} is {capital}.")
else:
    print(f"Sorry, I don't know the capital of {country}.")
```

Output:

```text
Country: japan
The capital of Japan is Tokyo.
```

`title` turns `japan` into `Japan`, matching the key. `get` returns `None` for a country that isn't in the dictionary, and `None` is falsy, so the `else` branch would handle it without any `KeyError`.

## Exercise 7.2

*Count each letter in `"mississippi"` and print the letters in alphabetical order with their counts.*

```python
counts = {}
for letter in "mississippi":
    counts[letter] = counts.get(letter, 0) + 1
for letter in sorted(counts):
    print(letter, counts[letter])
```

Output:

```text
i 4
m 1
p 2
s 4
```

The counting pattern gives a dictionary of four letters. `sorted(counts)` sorts the keys, so the letters come out in alphabetical order.

## Exercise 7.3

*Print the name with the highest score, the average, and everyone above the average.*

```python
scores = {"Asha": 88, "Ben": 52, "Chen": 92, "Dina": 67}
best = max(scores, key=scores.get)
average = sum(scores.values()) / len(scores)
above = []
for name, score in scores.items():
    if score > average:
        above.append(name)
print(f"Top: {best} ({scores[best]}), average {average:.2f}")
print("Above average:", above)
```

Output:

```text
Top: Chen (92), average 74.75
Above average: ['Asha', 'Chen']
```

`max(scores, key=scores.get)` goes through the names and compares them by their scores, returning the name, not the score. That is the same idiom as `sorted(..., key=d.get)` in the chapter. The average is 74.75, and Asha and Chen are above it.

## Exercise 7.4

*Invert `{"a": 1, "b": 2, "c": 1}` into `{1: ["a", "c"], 2: ["b"]}`.*

```python
original = {"a": 1, "b": 2, "c": 1}
inverted = {}
for key, value in original.items():
    if value not in inverted:
        inverted[value] = []
    inverted[value].append(key)
print(inverted)
```

Output:

```text
{1: ['a', 'c'], 2: ['b']}
```

This is the grouping pattern from the chapter: each old value becomes a key, and the old keys are collected in a list. A list is needed because several keys can share the same value.

## Exercise 7.5

*Use sets to compare two friends' movies.*

```python
asha = {"Inception", "Coco", "Up", "Dune"}
ravi = {"Dune", "Up", "Jaws", "Heat", "Coco"}
print("Both:", sorted(asha & ravi))
print("Only Asha:", sorted(asha - ravi))
print("Different movies in total:", len(asha | ravi))
```

Output:

```text
Both: ['Coco', 'Dune', 'Up']
Only Asha: ['Inception']
Different movies in total: 6
```

The intersection holds the movies both have seen, the difference the ones only Asha has seen, and the size of the union counts each movie once, even if both have seen it: six in all. `sorted` makes the output order predictable.

## Exercise 7.6

*Store three contacts as a list of dictionaries, print them as a table, and look up an email by name.*

```python
contacts = [
    {"name": "Asha Rao", "phone": "555-0101", "email": "asha@example.com"},
    {"name": "Ravi Kumar", "phone": "555-0102", "email": "ravi@example.org"},
    {"name": "Mei Lin", "phone": "555-0103", "email": "mei@example.net"},
]
for c in contacts:
    print(f"{c['name']:<12}{c['phone']:<10}{c['email']}")
wanted = input("Name: ").strip().lower()
for c in contacts:
    if wanted in c["name"].lower():
        print(c["name"], "->", c["email"])
```

Output:

```text
Asha Rao    555-0101  asha@example.com
Ravi Kumar  555-0102  ravi@example.org
Mei Lin     555-0103  mei@example.net
Name: RAVI
Ravi Kumar -> ravi@example.org
```

The table uses fixed widths for the first two columns. The search lowercases both the typed text and each name, so `RAVI` matches `Ravi Kumar`, and `in` lets the user type just part of a name.

## Exercise 7.7

*Group the words of a sentence by length, and print the groups from the shortest words to the longest, each in alphabetical order without duplicates.*

```python
sentence = "the quick brown fox jumps over the lazy dog and the cat"
groups = {}
for word in sentence.split():
    groups.setdefault(len(word), set()).add(word)
for length in sorted(groups):
    print(length, sorted(groups[length]))
```

Output:

```text
3 ['and', 'cat', 'dog', 'fox', 'the']
4 ['lazy', 'over']
5 ['brown', 'jumps', 'quick']
```

Each length maps to a *set* of words, so the repeated `the` is stored only once. `setdefault` (shown in Chapter 11) creates the empty set the first time a length is seen; the `if ... not in` pattern from the chapter works just as well. Sorting the keys gives the lengths in order, and sorting each set gives its words in alphabetical order.
