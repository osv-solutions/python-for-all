"""Solutions to the Chapter 3 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch03_solutions.py

The explanations are in ch03_solutions.md."""

# %% Exercise 3.1
s = "programming"
print(s[3], s[-2], s[3:7], s[:4])
print(s[::3], s.count("m"), s.find("g"), s.upper())

# %% Exercise 3.2
x = 1234.5
print(f"{x:.2f}")
print(f"{x:,.2f}")
print(f"[{x:>12}]")
print(f"{x:010.1f}")
print(f"{x / 10_000:.1%}")

# %% Exercise 3.3
sentence = input("Sentence: ")
print(sentence.replace(" ", "_"))
print("Words:", len(sentence.split()))
print("Characters without spaces:", len(sentence.replace(" ", "")))

# %% Exercise 3.4
text = input("Date (DD/MM/YYYY): ").strip()
day, month, year = text.split("/")
print(f"{year}-{month}-{day}")
print(f"{text[6:]}-{text[3:5]}-{text[:2]}")

# %% Exercise 3.5
word = input("Word: ").strip().lower()
print(word == word[::-1])

# %% Exercise 3.6
subtotal = 2 * 3.5 + 1 * 2.25 + 3 * 4.0
tax = subtotal * 0.06
print(f"{'Item':<12}{'Qty':>5}{'Price':>10}")
print("-" * 27)
print(f"{'Coffee':<12}{2:>5}{3.5:>10.2f}")
print(f"{'Bagel':<12}{1:>5}{2.25:>10.2f}")
print(f"{'Orange juice':<12}{3:>5}{4.0:>10.2f}")
print("-" * 27)
print(f"{'Subtotal':<12}{subtotal:>15.2f}")
print(f"{'Tax (6%)':<12}{tax:>15.2f}")
print(f"{'Total':<12}{subtotal + tax:>15.2f}")

# %% Exercise 3.7
parts = input("Full name: ").strip().title().split()
initials = parts[0][0] + "." + parts[1][0] + "." + parts[2][0] + "."
print(initials)
print(parts[2] + ", " + parts[0] + " " + parts[1])
print(parts[-1] + ", " + " ".join(parts[:-1]))
