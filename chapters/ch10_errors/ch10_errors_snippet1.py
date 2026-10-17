"""Code from "10.6 Debugging" that is shown in the book but not run on its own:
it needs your own data, a server or extra setup, or it is one step of an example
that the book builds up gradually. See the book for details."""

def average(numbers):
    total = 0
    for n in numbers:
        total += n
    breakpoint()

    return total / len(numbers)

print(average([4, 8, 6]))
