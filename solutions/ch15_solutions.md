# Solutions: Chapter 15, Functional Tools and Decorators

Worked solutions to the exercises at the end of Chapter 15 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch15_solutions.ipynb`](ch15_solutions.ipynb) or the script `ch15_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 15.1

*Sort a list of `(city, population)` tuples by population, largest first, with a lambda, then print the city with the smallest population using `min`.*

```python
cities = [("Lisbon", 545_000), ("Nairobi", 4_400_000),
          ("Lima", 10_000_000), ("Oslo", 710_000)]
by_size = sorted(cities, key=lambda c: c[1], reverse=True)
for city, population in by_size:
    print(f"{city:<8}{population:>11,}")
smallest = min(cities, key=lambda c: c[1])
print("Smallest:", smallest[0])
```

Output:

```text
Lima     10,000,000
Nairobi   4,400,000
Oslo        710,000
Lisbon      545,000
Smallest: Lisbon
```

The populations are rounded. `lambda c: c[1]` takes one tuple and returns its second item, so both `sorted` and `min` compare the cities by population instead of by name. `reverse=True` puts the largest, Lima, first. `min` returns the whole tuple with the smallest population, and `[0]` takes its name: Lisbon. The `,` in the format specification adds the thousands separators.

## Exercise 15.2

*Write `make_greeter(greeting)` that returns a function taking a name, so that `hello("Asha")` returns `"Hello, Asha!"`.*

```python
def make_greeter(greeting):
    def greet(name):
        return f"{greeting}, {name}!"
    return greet

hello = make_greeter("Hello")
namaste = make_greeter("Namaste")
print(hello("Asha"))
print(namaste("Ravi"), hello("Ben"))
```

Output:

```text
Hello, Asha!
Namaste, Ravi! Hello, Ben!
```

Each call to `make_greeter` creates a new `greet` function, a closure that remembers its own `greeting`. `hello` and `namaste` are two separate functions made from the same template, and using one doesn't affect the other. No `nonlocal` is needed, because `greet` only reads `greeting` and never assigns to it.

## Exercise 15.3

*Write a recursive function `count_files(tree)` for a nested dictionary in which folders are dictionaries and files are strings.*

```python
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
```

Output:

```text
3
0 1
```

The function has the same shape as `total` in the chapter. Each value is either a folder, which is a smaller copy of the problem and is counted by calling `count_files` on it, or a file, which counts as one. The base case is hidden in the loop: a folder with no subfolders makes no recursive calls. The example tree has 3 files. An empty tree has 0, and an empty folder adds nothing, so the last tree has 1.

## Exercise 15.4

*Write a decorator `timer` that prints how long each call took, using `time.perf_counter()`.*

```python
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
```

`time.perf_counter()` reads a precise clock, and the difference between two readings is the time in seconds that passed between them. The wrapper reads the clock before and after the call, prints the difference and returns the result. Let's time two functions:

```python
@timer
def slow_square(n):
    time.sleep(0.3)       # pretend this is a slow calculation
    return n * n

@timer
def sum_squares(limit):
    return sum(n * n for n in range(limit))

print(slow_square(12))
print(sum_squares(10_000))
```

Output:

```text
slow_square took 0.3 s
144
sum_squares took 0.0 s
333283335000
```

`time.sleep(0.3)` pauses the program for 0.3 seconds, so `slow_square` takes 0.3 seconds, and `sum_squares(10_000)` is so fast that it shows as 0.0. The exact times vary from run to run and from computer to computer, which is why this decorator prints only one decimal place: the output above is the same every time. To see the small differences, change the format to `{elapsed:.6f}`, which shows microseconds.

## Exercise 15.5

*Write a decorator `validate_positive` that raises a `ValueError` if any positional argument is negative, and apply it to `area(width, height)`.*

```python
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
```

The wrapper checks every positional argument before calling the function, so the function itself never sees a bad value. The `isinstance` test skips arguments that aren't numbers, such as a name, which could not be compared with 0 anyway. Let's test it:

```python
for width, height in [(3, 4.5), (3, -2), (0, 7)]:
    try:
        print(area(width, height))
    except ValueError as err:
        print("Error:", err)
```

Output:

```text
13.5
Error: area() got a negative number: -2
0
```

The first rectangle has an area of 13.5. The second call never reaches `area`: the wrapper finds the `-2` and raises the error, whose message names the function thanks to `func.__name__`. A width of 0 is allowed, giving an area of 0, because the exercise asks to reject only negative numbers; changing `value < 0` to `value <= 0` would reject zero too.

## Exercise 15.6

*Use `functools.lru_cache` on a recursive function that counts the ways to climb a staircase of `n` steps, one or two steps at a time.*

```python
@functools.lru_cache(maxsize=None)
def ways(n):
    """Return the number of ways to climb n steps by 1s and 2s."""
    if n <= 1:
        return 1                       # no steps, or a single step
    return ways(n - 1) + ways(n - 2)

print(ways(30))
print(ways.cache_info())
```

Output:

```text
1346269
CacheInfo(hits=28, misses=31, maxsize=None, currsize=31)
```

The first move is either one step, leaving `n - 1` steps to climb, or two steps, leaving `n - 2`, so the number of ways is the sum of the two smaller answers. With 0 or 1 steps there is exactly one way, which is the base case. Small staircases are easy to check by hand: 3 steps can be climbed as 1+1+1, 1+2 or 2+1, three ways. For 30 steps there are 1,346,269 ways. `cache_info()` shows 31 misses, one for each `n` from 30 down to 0, and 28 hits, the calls answered from the cache. Without the cache, the same function would make more than 2.6 million calls; these are the Fibonacci numbers again, in disguise.

## Exercise 15.7

*Extend the command registry so that each command stores a one-line help text, and add a `help` command that lists the commands sorted by name.*

```python
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
```

Each entry of `COMMANDS` is now a tuple of the function and its help text. The `help` command is registered in exactly the same way as the others:

```python
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
```

Output:

```text
5.5
HELLO THERE
  add    add two numbers
  help   list the commands
  upper  repeat the words in capitals
unknown command 'shout'; try help
```

The first two commands give 5.5 and `HELLO THERE` as before. The function is called `show_help` because the name `help` already belongs to Python's built-in `help` function, but it is registered under the command name `help`. `sorted(COMMANDS.items())` sorts the pairs by name, and the list comprehension unpacks each pair into the name and the `(func, text)` tuple. The list is built when `help` runs, not when it is defined, so it includes every command, `help` itself among them, and any command registered later will appear automatically. The dispatcher unpacks the tuple to find the function, and the unknown `shout` now points the user to `help`.
