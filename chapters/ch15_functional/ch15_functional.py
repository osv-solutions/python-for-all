"""Chapter 15: Functional Tools and Decorators

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch15_functional.py

or open the notebook and run the cells in order.
"""

# %% 15.1 Small functions with lambda
square = lambda x: x * x
print(square(7))
students = [("Asha", 88), ("Ben", 52), ("Chen", 92)]
print(sorted(students, key=lambda s: s[1], reverse=True))
print(min(students, key=lambda s: s[1]))

# %% 15.1 Small functions with lambda
words = ["kiwi", "Fig", "apple", "date", "Banana"]
print(sorted(words, key=lambda w: (len(w), w.lower())))

# %% 15.2 map and filter
numbers = "4 8 15 16 23 42".split()
values = list(map(int, numbers))
print(values)
print(list(filter(lambda n: n % 2 == 0, values)))
print(list(map(str.upper, ["a", "b", "c"])))

# %% 15.3 Functions that return functions: closures
def make_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(10), triple(10))
print([double(n) for n in range(4)])

# %% 15.3 Functions that return functions: closures
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

next_ticket = make_counter()
print(next_ticket(), next_ticket(), next_ticket())

# %% 15.4 Functions that call themselves: recursion
def factorial(n):
    """Return n! for a whole number n >= 0."""
    if n <= 1:
        return 1                         # the base case
    return n * factorial(n - 1)          # the recursive case

print(factorial(5), factorial(20))

# %% 15.4 Functions that call themselves: recursion
def total(items):
    """Add up all the numbers in a list of numbers and lists."""
    result = 0
    for item in items:
        if isinstance(item, list):
            result += total(item)    # a smaller copy of the problem
        else:
            result += item
    return result

print(total([1, [2, 3], [4, [5, [6]]]]))

# %% 15.5 Decorators
def logged(func):
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}{args}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper

# %% 15.5 Decorators
@logged
def add(a, b):
    return a + b

print(add(2, 3) * 10)

# %% 15.5 Decorators
import functools

def counted(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper

@counted
def greet(name):
    """Return a greeting."""
    return f"Hello, {name}!"

# %% 15.5 Decorators
greet("Asha")
greet("Ben")
print(greet.calls, greet.__name__, greet.__doc__)

# %% 15.5 Decorators
def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError as err:
                    print(f"  attempt {attempt} failed: {err}")
            raise ConnectionError(f"gave up after {times} attempts")
        return wrapper
    return decorator

# %% 15.5 Decorators
attempts = []

@retry(3)
def fetch_data():
    attempts.append(1)
    if len(attempts) < 3:
        raise ConnectionError("server busy")
    return "data received"

print(fetch_data())

# %% 15.6 More tools in functools
@functools.lru_cache(maxsize=None)
def fib(n):
    """Return the nth Fibonacci number."""
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(90))
print(fib.cache_info())

# %% 15.6 More tools in functools
from functools import partial

to_binary = partial(int, base=2)
print(to_binary("1010"), to_binary("11111111"))

# %% 15.7 Putting it together: a command registry
COMMANDS = {}

def command(name):
    """Register the decorated function under a command name."""
    def register(func):
        COMMANDS[name] = func
        return func
    return register

@command("add")
def add(a, b):
    return float(a) + float(b)

@command("upper")
def upper(*words):
    return " ".join(words).upper()

# %% 15.7 Putting it together: a command registry
def run(line):
    name, *args = line.split()
    func = COMMANDS.get(name)
    if func is None:
        return f"unknown command {name!r}; try {', '.join(COMMANDS)}"
    return func(*args)

for line in ["add 2 3.5", "upper hello there", "shout hi"]:
    print(run(line))
