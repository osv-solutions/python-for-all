# Solutions: Chapter 21, Doing Many Things at Once

Worked solutions to the exercises at the end of Chapter 21 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch21_solutions.ipynb`](ch21_solutions.ipynb) or the script `ch21_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

The timings below are printed rounded to one decimal place, as in the chapter; on your computer the exact times differ by a few thousandths of a second. The files for Exercise 21.6 are in `examples/ch21_solutions/` in the companion repository.

## Exercise 21.1

*Classify five tasks as I/O-bound or CPU-bound, and name the tool you would try.*

| Task | Kind | Tool to try | |---|---|---| | Resizing 500 photos with pure Python code | CPU-bound | `ProcessPoolExecutor` | | Checking that 200 web links still work | I/O-bound | `ThreadPoolExecutor` (with `requests`) or `asyncio` (with `httpx`) | | Computing the first 10,000 digits of pi | CPU-bound | None, or processes if it is too slow | | Copying files to a network drive | I/O-bound | `ThreadPoolExecutor` | | Asking a weather API for 30 cities | I/O-bound | `ThreadPoolExecutor` or `asyncio` |

The question to ask of each task is: while it runs, is the processor busy, or is it waiting for something outside the program? Resizing photos is arithmetic on millions of pixels, so it keeps a core busy; it gets faster only with more cores, so processes. (In practice you would use an image library written in C, which is much faster still.) The link checker and the weather lookups spend nearly all their time waiting for servers to answer, and copying to a network drive waits for the network and the disk, so threads or `asyncio` let the waits overlap. Computing digits of pi is CPU-bound, but the usual methods compute it as one long calculation in which each step builds on the one before, so it doesn't split easily into independent chunks; the simplest program is the right one unless it is too slow.

## Exercise 21.2

*Simulate breakfast (toast 0.4 s, coffee 0.3 s, eggs 0.5 s) one item after another, then with a `ThreadPoolExecutor`.*

```python
import time
from concurrent.futures import ThreadPoolExecutor

BREAKFAST = {"toast": 0.4, "coffee": 0.3, "eggs": 0.5}


def make(item):
    time.sleep(BREAKFAST[item])
    return item
```

`make` waits as long as the item takes and returns its name. First one item after another, then with a pool:

```python
start = time.perf_counter()
ready = [make(item) for item in BREAKFAST]
print(ready, f"after about {time.perf_counter() - start:.1f} s")

start = time.perf_counter()
with ThreadPoolExecutor() as pool:
    ready = list(pool.map(make, BREAKFAST))
print(ready, f"after about {time.perf_counter() - start:.1f} s")
```

Output:

```text
['toast', 'coffee', 'eggs'] after about 1.2 s
['toast', 'coffee', 'eggs'] after about 0.5 s
```

One item after another, breakfast takes the sum of the waits, about 1.2 s. With the thread pool, the three waits overlap and breakfast is ready after about 0.5 s, the time of the slowest item, the eggs. Both lists show the items in the same order, `['toast', 'coffee', 'eggs']`, because `pool.map` returns the results in the order of the input, not in the order they finished.

## Exercise 21.3

*Check pretend websites with `submit` and `as_completed`, printing each result or error in the order they finish.*

```python
from concurrent.futures import as_completed

SITES = {"python.org": 0.3, "example.com": 0.1,
         "gone.invalid": None, "pypi.org": 0.2}


def check(site):
    delay = SITES[site]
    if delay is None:
        raise ConnectionError(f"{site} did not answer")
    time.sleep(delay)
    return site, "ok"
```

`check` raises a `ConnectionError` straight away for a site without a delay, and otherwise waits and returns a tuple. The pool runs all four checks:

```python
with ThreadPoolExecutor() as pool:
    futures = [pool.submit(check, site) for site in SITES]
    for future in as_completed(futures):
        try:
            print(future.result())
        except ConnectionError as error:
            print("error:", error)
```

Output:

```text
error: gone.invalid did not answer
('example.com', 'ok')
('pypi.org', 'ok')
('python.org', 'ok')
```

The failing site raises its error at once, so its future is the first to complete, and `future.result()` raises the same `ConnectionError` in the main thread, where the `try` statement catches it: `error: gone.invalid did not answer`. The other results follow in the order of their delays: `('example.com', 'ok')` after 0.1 s, `('pypi.org', 'ok')` after 0.2 s and `('python.org', 'ok')` last. An error in one task doesn't stop the others; each future carries either its result or its exception.

## Exercise 21.4

*A `BankAccount` whose `deposit` reads, sleeps and writes loses money with ten threads; fix it with a lock.*

```python
import threading


class BankAccount:
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        seen = self.balance
        time.sleep(0.05)
        self.balance = seen + amount
```

`deposit` has the same read, pause and write as `Counter.add_one` in the chapter. A helper runs ten deposits of 10 in ten threads and returns the balance:

```python
def deposit_ten_times(account):
    threads = [threading.Thread(target=account.deposit, args=(10,))
               for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return account.balance


print(deposit_ten_times(BankAccount()))
```

Output:

```text
10
```

Ten deposits of 10 should give 100, but the balance is 10: all ten threads read 0 before any of them wrote, and each wrote 0 + 10. Ninety dollars vanished. The fix makes reading and writing one step with a lock, in a subclass:

```python
class SafeBankAccount(BankAccount):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()

    def deposit(self, amount):
        with self.lock:
            super().deposit(amount)


print(deposit_ten_times(SafeBankAccount()))
```

Output:

```text
100
```

Now the balance is 100. `SafeBankAccount.deposit` takes the lock and then calls the original `deposit` through `super()`, so the reading, sleeping and writing all happen while the lock is held, and only one thread at a time can be inside. The deposits now run one after another, which takes about 0.5 s, but correctness comes first. In a real bank account the sleep isn't there and the gap is tiny, so without the lock money would disappear only occasionally, which is why such bugs are so hard to find.

## Exercise 21.5

*Breakfast with `asyncio`, a `TaskGroup` and `asyncio.sleep`; then under `asyncio.timeout(0.45)`.*

```python
import asyncio


async def cook(item):
    await asyncio.sleep(BREAKFAST[item])
    print(item, "is ready")
    return item
```

`cook` is the asynchronous version of `make`: it waits with `await asyncio.sleep`, so the event loop can run the other tasks meanwhile.

```python
async def breakfast():
    async with asyncio.TaskGroup() as group:
        for item in BREAKFAST:
            group.create_task(cook(item))


start = time.perf_counter()
asyncio.run(breakfast())
print(f"breakfast after about {time.perf_counter() - start:.1f} s")
```

Output:

```text
coffee is ready
toast is ready
eggs is ready
breakfast after about 0.5 s
```

The three tasks wait at the same time, so the items are ready in the order of their waits, `coffee`, `toast` and `eggs`, and breakfast is served after about 0.5 s, as with threads. The `async with` block of the task group doesn't end until all three tasks have finished. Now with a deadline:

```python
async def hurried_breakfast():
    try:
        async with asyncio.timeout(0.45):
            async with asyncio.TaskGroup() as group:
                for item in BREAKFAST:
                    group.create_task(cook(item))
    except TimeoutError:
        print("out of time: the eggs were cancelled")


asyncio.run(hurried_breakfast())
```

Output:

```text
coffee is ready
toast is ready
out of time: the eggs were cancelled
```

`cook` already prints each item as it becomes ready, so the output itself shows what made it: `coffee is ready` after 0.3 s and `toast is ready` after 0.4 s. At 0.45 s, `asyncio.timeout` cancels the task still waiting, the eggs, and raises `TimeoutError`, which the `except` clause catches. A cancelled task stops at the `await` where it was waiting, so the eggs never reach their `print`. If you need the finished items as a list, have `cook` append each item to a list it is given; with `asyncio` that is safe without a lock, because a task can't be interrupted between two lines that contain no `await`.

## Exercise 21.6

*Sum the primes in the four ranges of `count_primes.py` with a `ProcessPoolExecutor`, the worker in a module and the pool guarded.*

The worker module, `prime_sums.py`, is `primes.py` from the chapter with `count_primes` replaced:

```python
def sum_primes(start, stop):
    """Return the sum of the primes in range(start, stop)."""
    return sum(n for n in range(start, stop) if is_prime(n))
```

The script, `sum_primes_parallel.py`, saved in the same folder:

```python
"""Sum the primes below one million in four chunks, in parallel."""
from concurrent.futures import ProcessPoolExecutor

from prime_sums import sum_primes

STARTS = [0, 250_000, 500_000, 750_000]
STOPS = [250_000, 500_000, 750_000, 1_000_000]

if __name__ == "__main__":
    with ProcessPoolExecutor() as pool:
        sums = list(pool.map(sum_primes, STARTS, STOPS))
    for start, stop, total in zip(STARTS, STOPS, sums):
        print(f"{start:>7,} to {stop:>9,}: {total:>15,}")
    print(f"all primes below 1,000,000: {sum(sums):,}")
```

<details>
<summary>Setup code: recreates the data and helpers from the chapter (click to show)</summary>

```python
import subprocess
import sys
from pathlib import Path

Path("prime_sums.py").write_text('''"""Add up prime numbers: the worker for sum_primes_parallel.py."""


def is_prime(n):
    """Return True if n is a prime number."""
    if n < 2:
        return False
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False
    return True


def sum_primes(start, stop):
    """Return the sum of the primes in range(start, stop)."""
    return sum(n for n in range(start, stop) if is_prime(n))
''')
Path("sum_primes_parallel.py").write_text('''"""Sum the primes below one million in four chunks, in parallel."""
from concurrent.futures import ProcessPoolExecutor

from prime_sums import sum_primes

STARTS = [0, 250_000, 500_000, 750_000]
STOPS = [250_000, 500_000, 750_000, 1_000_000]

if __name__ == "__main__":
    with ProcessPoolExecutor() as pool:
        sums = list(pool.map(sum_primes, STARTS, STOPS))
    for start, stop, total in zip(STARTS, STOPS, sums):
        print(f"{start:>7,} to {stop:>9,}: {total:>15,}")
    print(f"all primes below 1,000,000: {sum(sums):,}")
''')
run = subprocess.run([sys.executable, "sum_primes_parallel.py"],
                     capture_output=True, text=True, check=True)
print(run.stdout, end="")
```

</details>

```bash
python sum_primes_parallel.py
```

```output
      0 to   250,000:   2,623,031,151
250,000 to   500,000:   7,291,205,044
500,000 to   750,000:  11,674,022,830
750,000 to 1,000,000:  15,962,142,998
all primes below 1,000,000: 37,550,402,023
```

The only change in the worker is `sum(n for ...)` instead of `sum(1 for ...)`: adding the primes themselves instead of one for each prime. The four sums grow from chunk to chunk although there are fewer primes in each, because the primes themselves get larger. The total, 37,550,402,023, is the well-known sum of all primes below one million, which is a good check that no chunk was lost or counted twice. The two rules of the chapter apply: `sum_primes` lives in a module, so the worker processes can import it, and the pool is created only under `if __name__ == "__main__":`. Python's integers never overflow, so the large sums need no special care.

## Exercise 21.7

*Download 10 pretend files of 0.3 s each with `asyncio`, never more than 3 at a time, using `asyncio.Semaphore`.*

Each round of at most three downloads takes 0.3 s, and 10 files need four rounds (3 + 3 + 3 + 1), so the prediction is about 4 x 0.3 = 1.2 s.

```python
async def polite_download(name, semaphore, log):
    async with semaphore:
        log.append(name)
        await asyncio.sleep(0.3)


async def download_all():
    semaphore = asyncio.Semaphore(3)
    log = []
    async with asyncio.TaskGroup() as group:
        for k in range(1, 11):
            job = polite_download(f"file{k}", semaphore, log)
            group.create_task(job)
    return log
```

Each task records its name in `log` at the moment it gets past the semaphore, so the log shows the order in which the downloads started.

```python
start = time.perf_counter()
log = asyncio.run(download_all())
print("started in order:", log[0], "...", log[-1])
print(f"took about {time.perf_counter() - start:.1f} s")
```

Output:

```text
started in order: file1 ... file10
took about 1.2 s
```

A **semaphore** is a counter of free places: `asyncio.Semaphore(3)` has three. `async with semaphore:` takes a place, waiting if none is free, and gives it back at the end of the block. All ten tasks start at once, but only three get past the `async with` at a time; the others wait at that line, which is an `await` point, so the event loop runs whoever can continue. The downloads start in order, from `file1` to `file10`, and the whole job took about 1.2 s, as predicted: slower than ten at once (0.3 s), but kinder to the server, and much faster than one at a time (3.0 s). Real programs use exactly this pattern to respect a website's or an API's limits.
