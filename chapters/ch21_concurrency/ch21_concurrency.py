"""Chapter 21: Doing Many Things at Once

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch21_concurrency.py

or open the notebook and run the cells in order.
"""

# %% 21.1 Waiting versus working
import time

FILES = {"a.csv": 0.5, "b.csv": 0.3, "c.csv": 0.4,
         "d.csv": 0.1, "e.csv": 0.2}


def download(name):
    """Pretend to download a file: wait, then return a note."""
    time.sleep(FILES[name])
    return f"{name} ({FILES[name]} s)"


start = time.perf_counter()
for name in FILES:
    print("got", download(name))
elapsed = time.perf_counter() - start
print(f"took about {elapsed:.1f} s")

# %% 21.2 Threads: several workers in one program
import threading


def worker(name):
    print("got", download(name))


threads = [threading.Thread(target=worker, args=(n,)) for n in FILES]
start = time.perf_counter()
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print(f"took about {time.perf_counter() - start:.1f} s")

# %% 21.2 Threads: several workers in one program
from concurrent.futures import ThreadPoolExecutor

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(download, FILES))
elapsed = time.perf_counter() - start
for line in results:
    print(line)
print(f"took about {elapsed:.1f} s")

# %% 21.2 Threads: several workers in one program
from concurrent.futures import as_completed

with ThreadPoolExecutor() as pool:
    futures = [pool.submit(download, name) for name in FILES]
    for future in as_completed(futures):
        print("finished", future.result())

# %% 21.3 Race conditions and locks
counter = 0
seen_by_a = counter      # thread A reads 0
seen_by_b = counter      # thread B reads 0 before A has written
counter = seen_by_a + 1  # A writes 1
counter = seen_by_b + 1  # B writes 1: A's update is lost
print(counter)

# %% 21.3 Race conditions and locks
class Counter:
    def __init__(self):
        self.value = 0

    def add_one(self):
        seen = self.value       # read
        time.sleep(0.1)         # ...meanwhile, other threads run
        self.value = seen + 1   # write


def run_in_threads(function, count):
    threads = [threading.Thread(target=function)
               for _ in range(count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

# %% 21.3 Race conditions and locks
counter = Counter()
run_in_threads(counter.add_one, 5)
print(counter.value)

# %% 21.3 Race conditions and locks
class SafeCounter(Counter):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()

    def add_one(self):
        with self.lock:
            seen = self.value
            time.sleep(0.1)
            self.value = seen + 1


counter = SafeCounter()
run_in_threads(counter.add_one, 5)
print(counter.value)

# %% 21.5 Processes for CPU-bound work
# Setup: recreates the context this solution builds on (not printed in the book).
from pathlib import Path
Path("primes.py").write_text('''"""Count prime numbers: slow, CPU-bound work on purpose."""


def is_prime(n):
    """Return True if n is a prime number."""
    if n < 2:
        return False
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False
    return True


def count_primes(start, stop):
    """Return how many primes are in range(start, stop)."""
    return sum(1 for n in range(start, stop) if is_prime(n))
''')
import importlib
importlib.invalidate_caches()

# %% 21.5 Processes for CPU-bound work
from primes import count_primes

starts = [0, 250_000, 500_000, 750_000]
stops = [250_000, 500_000, 750_000, 1_000_000]
counts = list(map(count_primes, starts, stops))
print(counts)
print(sum(counts))

# %% 21.5 Processes for CPU-bound work
# Setup: recreates the context this solution builds on (not printed in the book).
import subprocess
import sys
Path("count_primes.py").write_text('''"""Count the primes below one million on all CPU cores."""
from concurrent.futures import ProcessPoolExecutor

from primes import count_primes

STARTS = [0, 250_000, 500_000, 750_000]
STOPS = [250_000, 500_000, 750_000, 1_000_000]

if __name__ == "__main__":
    with ProcessPoolExecutor() as pool:
        counts = list(pool.map(count_primes, STARTS, STOPS))
    for start, count in zip(STARTS, counts):
        print(f"from {start:>7,}: {count:>6,} primes")
    print(f"total below 1,000,000: {sum(counts):,}")
''')
run = subprocess.run([sys.executable, "count_primes.py"],
                     capture_output=True, text=True, check=True)
print(run.stdout, end="")

# %% 21.6 asyncio: one thread, many waiting tasks
import asyncio


async def download_async(name):
    await asyncio.sleep(FILES[name])
    return f"{name} ({FILES[name]} s)"


job = download_async("a.csv")
print(type(job).__name__)
print(asyncio.run(job))

# %% 21.6 asyncio: one thread, many waiting tasks
async def main():
    jobs = [download_async(name) for name in FILES]
    return await asyncio.gather(*jobs)


start = time.perf_counter()
results = asyncio.run(main())
elapsed = time.perf_counter() - start
print(results[0], "...", results[-1])
print(f"took about {elapsed:.1f} s")

# %% 21.6 asyncio: one thread, many waiting tasks
async def fetch(name):
    result = await download_async(name)
    print("finished", result)
    return result


async def main():
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(fetch(name)) for name in FILES]
    print(len(tasks), "tasks done:", tasks[0].result())


asyncio.run(main())

# %% 21.6 asyncio: one thread, many waiting tasks
async def main():
    try:
        async with asyncio.timeout(0.35):
            async with asyncio.TaskGroup() as group:
                for name in FILES:
                    group.create_task(fetch(name))
    except TimeoutError:
        print("gave up after 0.35 s")


asyncio.run(main())

# %% 21.6 asyncio: one thread, many waiting tasks
async def blocking_download(name):
    time.sleep(FILES[name])     # blocks the event loop!
    return name


async def main():
    jobs = [blocking_download(name) for name in FILES]
    return await asyncio.gather(*jobs)


start = time.perf_counter()
asyncio.run(main())
print(f"took about {time.perf_counter() - start:.1f} s")

# %% 21.6 asyncio: one thread, many waiting tasks
async def threaded_download(name):
    return await asyncio.to_thread(download, name)


async def main():
    jobs = [threaded_download(name) for name in FILES]
    return await asyncio.gather(*jobs)


start = time.perf_counter()
results = asyncio.run(main())
print(f"took about {time.perf_counter() - start:.1f} s")

# %% 21.6 asyncio: one thread, many waiting tasks
# Setup: recreates the context this solution builds on (not printed in the book).
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VERSIONS = {"requests": "2.34.2", "httpx": "0.28.1",
            "pytest": "9.1.1", "ruff": "0.16.10", "mypy": "2.4.0"}


class FakePyPI(BaseHTTPRequestHandler):
    def do_GET(self):
        name = self.path.strip("/").split("/")[1]
        time.sleep(0.3)
        info = {"name": name, "version": VERSIONS.get(name, "?")}
        body = json.dumps({"info": info}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


server = ThreadingHTTPServer(("127.0.0.1", 8021), FakePyPI)
threading.Thread(target=server.serve_forever, daemon=True).start()


async def warm_up():          # load httpx's parts before timing
    import httpx
    async with httpx.AsyncClient() as client:
        await client.get("http://127.0.0.1:8021/pypi/x/json")

asyncio.run(warm_up())

# %% 21.6 asyncio: one thread, many waiting tasks
import httpx

BASE = "http://127.0.0.1:8021"     # the real one: https://pypi.org
PACKAGES = ["requests", "httpx", "pytest", "ruff", "mypy"]


async def latest_version(client, name):
    response = await client.get(f"/pypi/{name}/json")
    response.raise_for_status()
    return response.json()["info"]["version"]


async def main():
    async with httpx.AsyncClient(base_url=BASE) as client:
        jobs = [latest_version(client, p) for p in PACKAGES]
        return await asyncio.gather(*jobs)

# %% 21.6 asyncio: one thread, many waiting tasks
start = time.perf_counter()
versions = asyncio.run(main())
elapsed = time.perf_counter() - start
for name, version in zip(PACKAGES, versions):
    print(f"{name:<10}{version}")
print(f"took about {elapsed:.1f} s")
