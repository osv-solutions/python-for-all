"""Solutions to the Chapter 21 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch21_solutions.py

The explanations are in ch21_solutions.md."""

# %% Exercise 21.2
import time
from concurrent.futures import ThreadPoolExecutor

BREAKFAST = {"toast": 0.4, "coffee": 0.3, "eggs": 0.5}


def make(item):
    time.sleep(BREAKFAST[item])
    return item

# %% Exercise 21.2
start = time.perf_counter()
ready = [make(item) for item in BREAKFAST]
print(ready, f"after about {time.perf_counter() - start:.1f} s")

start = time.perf_counter()
with ThreadPoolExecutor() as pool:
    ready = list(pool.map(make, BREAKFAST))
print(ready, f"after about {time.perf_counter() - start:.1f} s")

# %% Exercise 21.3
from concurrent.futures import as_completed

SITES = {"python.org": 0.3, "example.com": 0.1,
         "gone.invalid": None, "pypi.org": 0.2}


def check(site):
    delay = SITES[site]
    if delay is None:
        raise ConnectionError(f"{site} did not answer")
    time.sleep(delay)
    return site, "ok"

# %% Exercise 21.3
with ThreadPoolExecutor() as pool:
    futures = [pool.submit(check, site) for site in SITES]
    for future in as_completed(futures):
        try:
            print(future.result())
        except ConnectionError as error:
            print("error:", error)

# %% Exercise 21.4
import threading


class BankAccount:
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        seen = self.balance
        time.sleep(0.05)
        self.balance = seen + amount

# %% Exercise 21.4
def deposit_ten_times(account):
    threads = [threading.Thread(target=account.deposit, args=(10,))
               for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return account.balance


print(deposit_ten_times(BankAccount()))

# %% Exercise 21.4
class SafeBankAccount(BankAccount):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()

    def deposit(self, amount):
        with self.lock:
            super().deposit(amount)


print(deposit_ten_times(SafeBankAccount()))

# %% Exercise 21.5
import asyncio


async def cook(item):
    await asyncio.sleep(BREAKFAST[item])
    print(item, "is ready")
    return item

# %% Exercise 21.5
async def breakfast():
    async with asyncio.TaskGroup() as group:
        for item in BREAKFAST:
            group.create_task(cook(item))


start = time.perf_counter()
asyncio.run(breakfast())
print(f"breakfast after about {time.perf_counter() - start:.1f} s")

# %% Exercise 21.5
async def hurried_breakfast():
    try:
        async with asyncio.timeout(0.45):
            async with asyncio.TaskGroup() as group:
                for item in BREAKFAST:
                    group.create_task(cook(item))
    except TimeoutError:
        print("out of time: the eggs were cancelled")


asyncio.run(hurried_breakfast())

# %% Exercise 21.6
# Setup: recreates the context these solutions build on (from the chapter).
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

# %% Exercise 21.7
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

# %% Exercise 21.7
start = time.perf_counter()
log = asyncio.run(download_all())
print("started in order:", log[0], "...", log[-1])
print(f"took about {time.perf_counter() - start:.1f} s")
