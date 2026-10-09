"""Solutions to the Chapter 7 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch07_solutions.py

The explanations are in ch07_solutions.md."""

# %% Exercise 7.1
capitals = {"France": "Paris", "Japan": "Tokyo", "Kenya": "Nairobi",
            "Peru": "Lima", "India": "New Delhi"}
country = input("Country: ").strip().title()
capital = capitals.get(country)
if capital:
    print(f"The capital of {country} is {capital}.")
else:
    print(f"Sorry, I don't know the capital of {country}.")

# %% Exercise 7.2
counts = {}
for letter in "mississippi":
    counts[letter] = counts.get(letter, 0) + 1
for letter in sorted(counts):
    print(letter, counts[letter])

# %% Exercise 7.3
scores = {"Asha": 88, "Ben": 52, "Chen": 92, "Dina": 67}
best = max(scores, key=scores.get)
average = sum(scores.values()) / len(scores)
above = []
for name, score in scores.items():
    if score > average:
        above.append(name)
print(f"Top: {best} ({scores[best]}), average {average:.2f}")
print("Above average:", above)

# %% Exercise 7.4
original = {"a": 1, "b": 2, "c": 1}
inverted = {}
for key, value in original.items():
    if value not in inverted:
        inverted[value] = []
    inverted[value].append(key)
print(inverted)

# %% Exercise 7.5
asha = {"Inception", "Coco", "Up", "Dune"}
ravi = {"Dune", "Up", "Jaws", "Heat", "Coco"}
print("Both:", sorted(asha & ravi))
print("Only Asha:", sorted(asha - ravi))
print("Different movies in total:", len(asha | ravi))

# %% Exercise 7.6
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

# %% Exercise 7.7
sentence = "the quick brown fox jumps over the lazy dog and the cat"
groups = {}
for word in sentence.split():
    groups.setdefault(len(word), set()).add(word)
for length in sorted(groups):
    print(length, sorted(groups[length]))
