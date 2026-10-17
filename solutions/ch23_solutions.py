"""Solutions to the Chapter 23 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch23_solutions.py

The explanations are in ch23_solutions.md."""

# %% Exercise 23.4
def describe(text):
    """Return a summary such as '2 words, 9 characters'."""
    words = len(text.split())
    return (f"{words} word{'' if words == 1 else 's'}, "
            f"{len(text)} characters")

print(describe(""))
print(describe("Hello"))
print(describe("Hello there,\n  Ada"))
