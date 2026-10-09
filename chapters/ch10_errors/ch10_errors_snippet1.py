"""Code from "10.6 Debugging" that is shown in the book but not run automatically:
it needs your own data, a server or extra setup. See the book for details."""

def average(numbers):
    total = 0
    for n in numbers:
        total += n
    breakpoint()
    return total / len(numbers)

print(average([4, 8, 6]))
