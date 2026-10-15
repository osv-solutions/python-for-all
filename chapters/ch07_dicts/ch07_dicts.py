"""Chapter 7: Dictionaries and Sets

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch07_dicts.py

or open the notebook and run the cells in order.
"""

# %% 7.1 Looking things up by key
ages = {"Asha": 34, "Ben": 29, "Chen": 41}
print(ages["Ben"])
print(len(ages), type(ages))
print(ages)

# %% 7.1 Looking things up by key
# This example stops with an error on purpose (see the book).
try:
    ages = {"Asha": 34, "Ben": 29, "Chen": 41}
    print(ages["Dina"])
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% 7.2 Changing a dictionary
stock = {"apples": 12, "pears": 5}
stock["plums"] = 20
stock["apples"] = 9
stock["pears"] += 3
del stock["plums"]
print(stock)

# %% 7.2 Changing a dictionary
print("pears" in stock, "kiwis" in stock)
print(stock.get("apples"), stock.get("kiwis"))
print(stock.get("kiwis", 0))
removed = stock.pop("apples")
print(removed, stock)

# %% 7.3 Looping over a dictionary
capitals = {"India": "New Delhi", "Japan": "Tokyo",
            "United States": "Washington, D.C.",
            "England": "London"}
for country in capitals:
    print(country)
print()
for country, city in capitals.items():
    print(f"{country}: {city}")

# %% 7.3 Looping over a dictionary
prices = {"tea": 2.50, "cake": 3.75, "soup": 5.25}
print(list(prices.keys()))
print(sum(prices.values()))
print(sorted(prices, key=prices.get, reverse=True))

# %% 7.4 Counting
votes = ["tea", "coffee", "tea", "juice", "coffee", "tea"]
counts = {}
for vote in votes:
    counts[vote] = counts.get(vote, 0) + 1
print(counts)

# %% 7.5 Grouping
words = ["apple", "bean", "avocado", "cherry", "banana", "corn"]
groups = {}
for word in words:
    letter = word[0]
    if letter not in groups:
        groups[letter] = []
    groups[letter].append(word)
for letter, group in groups.items():
    print(letter, group)

# %% 7.6 Nested data
books = [
    {"title": "Dune", "year": 1965, "tags": ["sci-fi", "classic"]},
    {"title": "Emma", "year": 1815, "tags": ["romance", "classic"]},
    {"title": "Holes", "year": 1998, "tags": ["children"]},
]
print(books[1]["title"], books[1]["tags"][0])
for book in books:
    if "classic" in book["tags"]:
        print(f"{book['title']} ({book['year']})")

# %% 7.7 Sets
visited = {"Paris", "Rome", "Paris", "Lisbon"}
print(len(visited))
visited.add("Oslo")
visited.add("Rome")
print(sorted(visited))
print("Rome" in visited, "Tokyo" in visited)

# %% 7.7 Sets
emails = ["a@x.com", "b@y.org", "a@x.com", "c@z.net", "b@y.org"]
unique = set(emails)
print(len(emails), "addresses,", len(unique), "unique")
print(sorted(unique))

# %% 7.7 Sets
python = {"Asha", "Ben", "Chen", "Dina"}
java = {"Chen", "Dina", "Eli"}
print(sorted(python | java))
print(sorted(python & java))
print(sorted(python - java))
print(sorted(python ^ java))

# %% 7.9 Putting it together: a word frequency report
text = """The cat sat on the mat. The dog sat on the log.
The cat saw the dog, and the dog saw the cat!"""
counts = {}
for word in text.lower().split():
    word = word.strip(".,!?")
    counts[word] = counts.get(word, 0) + 1
print(len(text.split()), "words,", len(counts), "different")

# %% 7.9 Putting it together: a word frequency report
top = sorted(counts, key=counts.get, reverse=True)[:4]
for word in top:
    print(f"{word:<6}{counts[word]:>3}  {'*' * counts[word]}")
print("Only once:", sorted(w for w in counts if counts[w] == 1))
