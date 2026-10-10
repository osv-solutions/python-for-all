"""Project 13 (Advanced): Website Uptime Checker with asyncio

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python p13_uptime.py

or open the notebook and run the cells in order.
"""

# %% Step 1: The sites to watch
# Setup: recreates the context this solution builds on (not printed in the book).
import asyncio
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class PracticeSites(BaseHTTPRequestHandler):
    health_hits = 0          # requests to /api/health so far

    def do_GET(self):
        if self.path == "/":
            self.answer(200, "Welcome to the practice shop!")
        elif self.path == "/shop":
            time.sleep(0.8)                  # a slow page
            self.answer(200, "Our products")
        elif self.path == "/api/health":     # down 3 times out of 6
            n = PracticeSites.health_hits
            PracticeSites.health_hits += 1
            if (n // 3) % 2 == 1:
                self.answer(503, "Down for maintenance")
            else:
                self.answer(200, "OK")
        elif self.path == "/old":            # moved to the home page
            self.send_response(301)
            self.send_header("Location", "/")
            self.send_header("Content-Length", "0")
            self.end_headers()
        elif self.path == "/hang":           # never answers in time
            time.sleep(3)
            self.answer(200, "Sorry, I was busy")
        else:
            self.answer(404, "No such page")

    def answer(self, status, text):
        data = text.encode("utf-8")
        try:
            self.send_response(status)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except OSError:          # the client gave up waiting
            pass

    def log_message(self, *args):
        pass                     # keep the terminal quiet


server = ThreadingHTTPServer(("127.0.0.1", 8111), PracticeSites)
threading.Thread(target=server.serve_forever, daemon=True).start()


async def warm_up():          # load httpx's parts before timing
    import httpx
    async with httpx.AsyncClient() as client:
        await client.get("http://127.0.0.1:8111/")

asyncio.run(warm_up())

# %% Step 1: The sites to watch
from pathlib import Path

Path("sites.txt").write_text("""\
# Practice sites, served by practice_server.py
http://127.0.0.1:8111/
http://127.0.0.1:8111/shop
http://127.0.0.1:8111/api/health
http://127.0.0.1:8111/old
http://127.0.0.1:8111/missing
http://127.0.0.1:8111/hang

# Nothing listens on port 8119:
http://127.0.0.1:8119/
""", encoding="utf-8")

# %% Step 1: The sites to watch
def read_sites(path: str) -> list[str]:
    """Return the URLs in a sites file, skipping comments."""
    sites = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            sites.append(line)
    return sites


SITES = read_sites("sites.txt")
print(len(SITES), "sites, the last:", SITES[-1])

# %% Step 2: One check
from dataclasses import dataclass


@dataclass
class CheckResult:
    url: str
    status: int | None    # None if there was no answer
    ok: bool              # a 2xx answer arrived in time
    speed: str            # "fast", "slow" or "-" (no answer)
    note: str = ""        # what went wrong, or "redirected"

    @property
    def state(self) -> str:
        return "UP" if self.ok else "DOWN"

# %% Step 2: One check
import asyncio
import time

import httpx

TIMEOUT = 1.0      # seconds to wait for an answer
SLOW = 0.5         # answers slower than this count as slow
AGENT = {"User-Agent": "ada-uptime/1.0 (ada@example.com)"}


def make_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=TIMEOUT, headers=AGENT,
                             follow_redirects=True)

# %% Step 2: One check
async def check(client: httpx.AsyncClient, url: str) -> CheckResult:
    start = time.perf_counter()
    try:
        response = await client.get(url)
    except httpx.TimeoutException:
        return CheckResult(url, None, False, "-", "timed out")
    except httpx.ConnectError:
        return CheckResult(url, None, False, "-", "cannot connect")
    except httpx.HTTPError as error:
        return CheckResult(url, None, False, "-",
                           type(error).__name__)
    seconds = time.perf_counter() - start
    speed = "slow" if seconds > SLOW else "fast"
    ok = response.is_success
    note = response.reason_phrase if not ok else (
        "redirected" if response.history else "")
    return CheckResult(url, response.status_code, ok, speed, note)

# %% Step 3: All sites at once
async def check_all(client: httpx.AsyncClient,
                    urls: list[str], limit: int = 3
                    ) -> list[CheckResult]:
    gate = asyncio.Semaphore(limit)

    async def limited(url: str) -> CheckResult:
        async with gate:                 # wait for a free place
            return await check(client, url)

    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(limited(u)) for u in urls]
    return [task.result() for task in tasks]

# %% Step 3: All sites at once
async def one_by_one(client: httpx.AsyncClient,
                     urls: list[str]) -> list[CheckResult]:
    return [await check(client, url) for url in urls]


async def timed(checker, urls: list[str]):
    start = time.perf_counter()
    async with make_client() as client:
        results = await checker(client, urls)
    return results, round(time.perf_counter() - start)

# %% Step 3: All sites at once
_, seconds = asyncio.run(timed(one_by_one, SITES))
print(f"One after another: about {seconds} s")
results, seconds = asyncio.run(timed(check_all, SITES))
print(f"At most 3 at once: about {seconds} s")

# %% Step 4: A report
def report(results: list[CheckResult]) -> None:
    print(f"{'Site':<33}{'Code':>5}  {'State':<6}{'Speed':<6}Note")
    for r in results:
        code = "-" if r.status is None else r.status
        print(f"{r.url:<33}{code:>5}  {r.state:<6}{r.speed:<6}"
              f"{r.note}")
    up = sum(r.ok for r in results)
    print(f"{up} of {len(results)} sites are up")


report(results)

# %% Step 5: Rounds and alerts
def alerts(previous: dict[str, bool],
           results: list[CheckResult]) -> list[str]:
    """Alert lines for sites whose state changed; update previous."""
    lines = []
    for r in results:
        before = previous.get(r.url)
        if before is not None and before != r.ok:
            why = "UP again" if r.ok else f"DOWN ({r.note})"
            lines.append(f"  ALERT {r.url} is {why}")
        previous[r.url] = r.ok
    return lines

# %% Step 5: Rounds and alerts
import csv


def append_log(path: str, n: int,
               results: list[CheckResult]) -> None:
    new = not Path(path).exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new:
            writer.writerow(["round", "url", "status", "ok", "speed"])
        for r in results:
            writer.writerow([n, r.url, r.status, r.ok, r.speed])

# %% Step 5: Rounds and alerts
async def monitor(sites: list[str], rounds: int, interval: float,
                  log: str) -> None:
    previous: dict[str, bool] = {}
    async with make_client() as client:
        for n in range(1, rounds + 1):
            results = await check_all(client, sites)
            up = sum(r.ok for r in results)
            print(f"Round {n}: {up} of {len(results)} up")
            for line in alerts(previous, results):
                print(line)
            append_log(log, n, results)
            if n < rounds:
                await asyncio.sleep(interval)

# %% Step 5: Rounds and alerts
asyncio.run(monitor(SITES, 5, 0.5, "uptime_log.csv"))

# %% Step 6: Uptime from the log
from collections import Counter


def uptime(log: str) -> dict[str, float]:
    """The percentage of checks in the log that each site passed."""
    checks, passed = Counter(), Counter()
    with open(log, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            checks[row["url"]] += 1
            passed[row["url"]] += row["ok"] == "True"
    return {url: 100 * passed[url] / checks[url] for url in checks}


percents = uptime("uptime_log.csv")
print(percents[SITES[0]], percents[SITES[2]], percents[SITES[4]])

# %% Step 7: The finished program
def main(sites_file: str = "sites.txt", rounds: int = 3,
         interval: float = 300, log: str = "uptime_log.csv") -> None:
    sites = read_sites(sites_file)
    print(f"Watching {len(sites)} sites, {rounds} rounds")
    asyncio.run(monitor(sites, rounds, interval, log))
    print("Uptime so far:")
    for url, percent in uptime(log).items():
        print(f"  {url:<33}{percent:6.1f}%")

# %% Step 7: The finished program
main(rounds=3, interval=0.5, log="demo_log.csv")

# %% Step 7: The finished program
# Setup: recreates the context this solution builds on (not printed in the book).
server.shutdown()
server.server_close()
