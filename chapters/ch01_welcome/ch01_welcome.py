"""Chapter 1: Welcome to Python

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch01_welcome.py

or open the notebook and run the cells in order.
"""

# %% 1.1 What is a program?
print("Hello, world!")

# %% 1.6 Your first program
print("Hello, world!")

# %% 1.6 Your first program
print("Welcome to Python for All.")
print("Programs run from top to bottom.")
print()
print("That empty line came from print() with no arguments.")

# %% 1.6 Your first program
print("Python", "was", "released", "in", 1991)
print("2 + 3 =", 2 + 3)
print("A", "B", "C", sep="-")

# %% 1.6 Your first program
# This program greets the reader.
print("Hello again!")  # a comment can follow code, too
# print("This line is switched off.")

# %% 1.7 When things go wrong
# This example contains a mistake on purpose (see the book).
# Python would refuse to run this whole file, so it is commented
# out. Copy it into a file of its own to see the error message:
# print("Hello, world!)


# %% 1.7 When things go wrong
# This example contains a mistake on purpose (see the book).
# Python would refuse to run this whole file, so it is commented
# out. Copy it into a file of its own to see the error message:
# print("Hello, world!"
# print("Goodbye")


# %% 1.7 When things go wrong
# This example stops with an error on purpose (see the book).
try:
    prnt("Hello, world!")
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% 1.7 When things go wrong
# This example stops with an error on purpose (see the book).
try:
    Print("Hello")
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% 1.7 When things go wrong
# This example contains a mistake on purpose (see the book).
# Python would refuse to run this whole file, so it is commented
# out. Copy it into a file of its own to see the error message:
# print(“Hello”)


# %% 1.8 Getting help from Python
print("Loading", end="...")
print("done")
