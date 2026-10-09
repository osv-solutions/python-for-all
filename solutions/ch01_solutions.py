"""Solutions to the Chapter 1 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch01_solutions.py

The explanations are in ch01_solutions.md."""

# %% Exercise 1.1
print(7 * 24 * 60)
print(24 * 60 * 60)

# %% Exercise 1.2
print("Name: Vamsi")
print("City: Visakhapatnam")
print("Favorite food: mango pickle")
print()
print("Thanks for reading!")

# %% Exercise 1.3
print(2026, "10", "08", sep="-")

# %% Exercise 1.4
# This example contains a mistake on purpose (see the book).
# Python would refuse to run this whole file, so it is commented
# out. Copy it into a file of its own to see the error message:
# print("Python is fun)


# %% Exercise 1.4
print("Python", "is" "fun")

# %% Exercise 1.4
# This example stops with an error on purpose (see the book).
try:
    pritn("Python is fun")
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% Exercise 1.4
# This example contains a mistake on purpose (see the book).
# Python would refuse to run this whole file, so it is commented
# out. Copy it into a file of its own to see the error message:
# print("Python is fun"))


# %% Exercise 1.5
print("Ready, set,", end=" ")
print("go!")

# %% Exercise 1.6
print("    /\\")
print("   /  \\")
print("  | () |")
print("  |    |")
print(" /|____|\\")
print("   /||\\")
