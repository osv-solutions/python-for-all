"""Chapter 3: Working with Text

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch03_text.py

The script asks you to type answers. To replay the answers used
in the book instead:

    python ch03_text.py < ch03_text.inputs.txt

You can also open the notebook and run the cells in order.
"""

# %% 3.1 Characters and positions
word = "Python"
print(word[0], word[1], word[5])
print(len(word))

# %% 3.1 Characters and positions
word = "Python"
print(word[-1], word[-2], word[-6])

# %% 3.1 Characters and positions
# This example stops with an error on purpose (see the book).
try:
    word = "Python"
    print(word[6])
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% 3.2 Slicing
word = "Python"
print(word[0:2])
print(word[2:6])
print(word[:2], word[2:])
print(word[-3:])

# %% 3.2 Slicing
letters = "abcdefghij"
print(letters[::2])
print(letters[1:8:3])
print(letters[::-1])

# %% 3.2 Slicing
# This example stops with an error on purpose (see the book).
try:
    word = "Python"
    word[0] = "J"
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% 3.2 Slicing
word = "Python"
word = "J" + word[1:]
print(word)

# %% 3.3 String methods
title = "the hitchhiker's guide"
print(title.upper())
print(title.title())
print(title.capitalize())
print("SHOUTING".lower())

# %% 3.3 String methods
raw = "   Ada Lovelace  "
print("[" + raw + "]")
print("[" + raw.strip() + "]")
print("2026-10-08".replace("-", "/"))
print("banana".replace("a", "o", 1))

# %% 3.3 String methods
typed = "  aDA   lovelace "
clean = typed.strip().title()
print(clean)

# %% 3.3 String methods
sentence = "the cat sat on the mat"
print(sentence.count("at"))
print(sentence.find("sat"), sentence.find("dog"))
print(sentence.startswith("the"), sentence.endswith("."))
print("cat" in sentence, "dog" not in sentence)

# %% 3.3 String methods
print("2026".isdigit(), "20.5".isdigit(), "".isdigit())
print("Python".isalpha(), "Python3".isalpha())
print("hello".islower(), "Hello".isupper())

# %% 3.4 Splitting and joining
print("  red   green blue ".split())
print("2026-10-08".split("-"))
words = "  aDA   lovelace ".split()
print(" ".join(words).title())

# %% 3.5 Special characters
print("Line one\nLine two")
print("Name:\tAda")
print("She said \"hi\" and left.")
print("A backslash: \\")

# %% 3.5 Special characters
poem = """Roses are red,
Violets are blue,
Python is readable,
And so are you."""
print(poem)
print(poem.count("\n"), "line breaks")

# %% 3.6 Formatting output with f-strings
name, items, price = "Ravi", 3, 4.5
print(f"{name} bought {items} items for ${items * price}.")
print(f"Name in capitals: {name.upper()}, {len(name)} letters")
print(f"{items=}, {price=}")

# %% 3.6 Formatting output with f-strings
pi = 3.14159265
print(f"[{pi:.2f}] [{pi:.4f}] [{pi:8.2f}]")
print(f"[{'left':<8}] [{'right':>8}] [{'center':^8}]")
print(f"[{42:05d}] [{7:*^7}]")

# %% 3.6 Formatting output with f-strings
population = 8_100_000_000
share = 0.2847
print(f"{population:,} people")
print(f"{share:.1%} of the total")
print(f"{1234567.891:,.2f}")

# %% 3.6 Formatting output with f-strings
print(f"{'Item':<12}{'Qty':>5}{'Price':>10}")
print("-" * 27)
print(f"{'Coffee':<12}{2:>5}{3.5:>10.2f}")
print(f"{'Bagel':<12}{1:>5}{2.25:>10.2f}")
print(f"{'Orange juice':<12}{3:>5}{4.0:>10.2f}")
print("-" * 27)
total = 2 * 3.5 + 1 * 2.25 + 3 * 4.0
print(f"{'Total':<12}{total:>15.2f}")

# %% 3.7 Putting it together: a username generator
first = input("First name: ").strip().title()
last = input("Last name: ").strip().title()

username = (first[0] + last).lower()
email = f"{username}@example.com"

print("+" + "-" * 30 + "+")
print(f"|{first + ' ' + last:^30}|")
print(f"|{'user: ' + username:^30}|")
print(f"|{email:^30}|")
print("+" + "-" * 30 + "+")
