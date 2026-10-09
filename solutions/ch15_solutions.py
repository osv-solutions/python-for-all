"""Solutions to the Chapter 15 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch15_solutions.py

The explanations are in ch15_solutions.md."""

# %% Exercise 15.1
cities = [("Lisbon", 545_000), ("Nairobi", 4_400_000),
          ("Lima", 10_000_000), ("Oslo", 710_000)]
by_size = sorted(cities, key=lambda c: c[1], reverse=True)
for city, population in by_size:
    print(f"{city:<8}{population:>11,}")
smallest = min(cities, key=lambda c: c[1])
print("Smallest:", smallest[0])

# %% Exercise 15.2
def make_greeter(greeting):
    def greet(name):
        return f"{greeting}, {name}!"
    return greet

hello = make_greeter("Hello")
namaste = make_greeter("Namaste")
print(hello("Asha"))
print(namaste("Ravi"), hello("Ben"))

# %% Exercise 15.3
def count_files(tree):
    """Return the number of files in a tree of nested dictionaries."""
    count = 0
    for item in tree.values():
        if isinstance(item, dict):
            count += count_files(item)    # a folder: count inside it
        else:
            count += 1                    # a file
    return count

tree = {"docs": {"a.txt": "x", "old": {"b.txt": "y"}}, "c.txt": "z"}
print(count_files(tree))
print(count_files({}), count_files({"empty": {}, "d.txt": "w"}))

# %% Exercise 15.4
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.1f} s")
        return result
    return wrapper

# %% Exercise 15.4
@timer
def slow_square(n):
    time.sleep(0.3)       # pretend this is a slow calculation
    return n * n

@timer
def sum_squares(limit):
    return sum(n * n for n in range(limit))

print(slow_square(12))
print(sum_squares(10_000))

# %% Exercise 15.5
def validate_positive(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for value in args:
            if isinstance(value, (int, float)) and value < 0:
                msg = f"{func.__name__}() got a negative number"
                raise ValueError(f"{msg}: {value}")
        return func(*args, **kwargs)
    return wrapper

@validate_positive
def area(width, height):
    return width * height

# %% Exercise 15.5
for width, height in [(3, 4.5), (3, -2), (0, 7)]:
    try:
        print(area(width, height))
    except ValueError as err:
        print("Error:", err)

# %% Exercise 15.6
@functools.lru_cache(maxsize=None)
def ways(n):
    """Return the number of ways to climb n steps by 1s and 2s."""
    if n <= 1:
        return 1                       # no steps, or a single step
    return ways(n - 1) + ways(n - 2)

print(ways(30))
print(ways.cache_info())

# %% Exercise 15.7
COMMANDS = {}

def command(name, help_text):
    """Register the function under a name, with a help text."""
    def register(func):
        COMMANDS[name] = (func, help_text)
        return func
    return register

@command("add", "add two numbers")
def add(a, b):
    return float(a) + float(b)

@command("upper", "repeat the words in capitals")
def upper(*words):
    return " ".join(words).upper()

# %% Exercise 15.7
@command("help", "list the commands")
def show_help():
    lines = [f"  {name:<7}{text}"
             for name, (func, text) in sorted(COMMANDS.items())]
    return "\n".join(lines)

def run(line):
    name, *args = line.split()
    if name not in COMMANDS:
        return f"unknown command {name!r}; try help"
    func, text = COMMANDS[name]
    return func(*args)

for line in ["add 2 3.5", "upper hello there", "help", "shout hi"]:
    print(run(line))
