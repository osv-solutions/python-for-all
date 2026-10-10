"""Project 15 (Advanced): Price Watch: a Web Scraper with a Database

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python p15_scraper.py

or open the notebook and run the cells in order.
"""

# %% Step 1: The shop and its rules
# Setup: recreates the context this solution builds on (not printed in the book).
# Starts the practice shop from the examples folder, as
# `python practice_server.py` would in a terminal of its own.
import sys
from pathlib import Path

for root in ("../../repo_static/examples", "../../examples"):
    folder = Path(root, "p15_bookshop")
    if folder.exists():
        sys.path.insert(0, str(folder.resolve()))
import practice_server

shop = practice_server.start(port=8115)
Path("prices.db").unlink(missing_ok=True)   # start fresh every run

# %% Step 1: The shop and its rules
from urllib.robotparser import RobotFileParser

BASE = "http://127.0.0.1:8115"
AGENT = "ada-price-watch/1.0 (ada@example.com)"

robots = RobotFileParser(f"{BASE}/robots.txt")
robots.read()
for path in ["/catalogue/page-1.html", "/checkout/add?book=dracula"]:
    print(path, robots.can_fetch(AGENT, BASE + path))
print("Crawl-delay:", robots.crawl_delay(AGENT))

# %% Step 2: A polite fetcher
import time
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

# %% Step 2: A polite fetcher
@dataclass
class Fetcher:
    session: requests.Session
    robots: RobotFileParser
    agent: str
    delay: float
    next_time: float = 0.0      # earliest time for the next request
    count: int = 0              # requests made so far
    def soup(self, url: str) -> BeautifulSoup:
        if not self.robots.can_fetch(self.agent, url):
            raise PermissionError(f"robots.txt forbids {url}")
        time.sleep(max(0.0, self.next_time - time.monotonic()))
        response = self.session.get(url, timeout=10)
        self.next_time = time.monotonic() + self.delay
        self.count += 1
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

# %% Step 2: A polite fetcher
def make_fetcher(base: str, agent: str) -> Fetcher:
    robots = RobotFileParser(f"{base}/robots.txt")
    robots.read()
    session = requests.Session()
    session.headers["User-Agent"] = agent
    delay = robots.crawl_delay(agent) or 1
    return Fetcher(session, robots, agent, float(delay))


fetcher = make_fetcher(BASE, AGENT)
page = fetcher.soup(f"{BASE}/catalogue/page-1.html")
print(page.title.get_text(), "|", fetcher.count, "request")

# %% Step 3: Reading the catalog
@dataclass(frozen=True)
class Listing:
    url: str
    title: str
    cents: int
    in_stock: bool


def parse_price(text: str) -> int:
    """'$12.99' -> 1299: money as whole cents, never as a float."""
    dollars, _, cents = text.strip().removeprefix("$").partition(".")
    return int(dollars) * 100 + int(cents.ljust(2, "0"))


def money(cents: int) -> str:
    return f"${cents // 100}.{cents % 100:02d}"

# %% Step 3: Reading the catalog
from urllib.parse import urljoin


def parse_catalog(soup: BeautifulSoup, page_url: str
                  ) -> list[Listing]:
    listings = []
    for pod in soup.select("article.product_pod"):
        link = pod.select_one("h3 a")
        price = pod.select_one(".price_color").get_text()
        listings.append(Listing(url=urljoin(page_url, link["href"]),
                                title=link["title"],
                                cents=parse_price(price),
                                in_stock=pod.select_one(".instock")
                                is not None))
    return listings

# %% Step 3: Reading the catalog
url = f"{BASE}/catalogue/page-1.html"
for item in parse_catalog(page, url)[:4]:
    stock = "in stock" if item.in_stock else "SOLD OUT"
    print(f"{item.title:<20} {money(item.cents):>7}  {stock}")
print(parse_catalog(page, url)[0].url)

# %% Step 4: Following the pages
from collections.abc import Iterator


def crawl(fetcher: Fetcher, start: str,
          max_pages: int = 20) -> Iterator[Listing]:
    url: str | None = start
    seen: set[str] = set()
    while url and url not in seen and len(seen) < max_pages:
        seen.add(url)
        soup = fetcher.soup(url)
        yield from parse_catalog(soup, url)
        link = soup.select_one("li.next a")
        url = urljoin(url, link["href"]) if link else None

# %% Step 4: Following the pages
fetcher = make_fetcher(BASE, AGENT)
start = time.monotonic()
books = list(crawl(fetcher, f"{BASE}/catalogue/page-1.html"))
seconds = time.monotonic() - start
print(len(books), "books from", fetcher.count, "pages")
print("Sold out:", [b.title for b in books if not b.in_stock])
print(f"Cheapest: {min(books, key=lambda b: b.cents).title}")
print("At least 2 seconds:", seconds >= 2)

# %% Step 5: The book pages
def parse_details(soup: BeautifulSoup) -> dict[str, str]:
    rows = soup.select("table.product_info tr")
    return {row.th.get_text(): row.td.get_text() for row in rows}


moby = next(b for b in books if b.title == "Moby-Dick")
details = parse_details(fetcher.soup(moby.url))
print(details)

# %% Step 6: The database
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    url      TEXT PRIMARY KEY,
    title    TEXT NOT NULL,
    author   TEXT,
    category TEXT
);
CREATE TABLE IF NOT EXISTS prices (
    url      TEXT NOT NULL REFERENCES books (url),
    seen_on  TEXT NOT NULL,
    cents    INTEGER NOT NULL,
    in_stock INTEGER NOT NULL,
    PRIMARY KEY (url, seen_on)
);
"""

# %% Step 6: The database
def open_db(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn

# %% Step 7: The first scrape
from datetime import date


def add_book(conn: sqlite3.Connection, fetcher: Fetcher,
             item: Listing) -> None:
    info = parse_details(fetcher.soup(item.url))
    conn.execute("INSERT INTO books VALUES (?, ?, ?, ?)",
                 (item.url, item.title, info.get("Author"),
                  info.get("Category")))

# %% Step 7: The first scrape
def scrape(conn: sqlite3.Connection, fetcher: Fetcher, day: date,
           start: str = f"{BASE}/catalogue/page-1.html") -> int:
    known = {url for (url,) in conn.execute("SELECT url FROM books")}
    count = 0
    with conn:                     # one transaction for the scrape
        for item in crawl(fetcher, start):
            if item.url not in known:
                add_book(conn, fetcher, item)
            conn.execute(
                "INSERT OR REPLACE INTO prices VALUES (?, ?, ?, ?)",
                (item.url, str(day), item.cents, item.in_stock))
            count += 1
    return count

# %% Step 7: The first scrape
conn = open_db("prices.db")
fetcher = make_fetcher(BASE, AGENT)
print(scrape(conn, fetcher, date(2026, 10, 5)), "books saved,",
      fetcher.count, "requests")
for row in conn.execute("SELECT category, COUNT(*), MIN(cents) "
                        "FROM books JOIN prices USING (url) "
                        "GROUP BY category ORDER BY category"):
    print(f"{row[0]:<16} {row[1]} books, from {money(row[2])}")

# %% Step 8: A week later
# Setup: recreates the context this solution builds on (not printed in the book).
practice_server.set_week(2)

# %% Step 8: A week later
fetcher = make_fetcher(BASE, AGENT)
print(scrape(conn, fetcher, date(2026, 10, 12)), "books saved,",
      fetcher.count, "requests")
for table in ["prices", "books"]:
    sql = f"SELECT COUNT(*) FROM {table}"
    print(table, conn.execute(sql).fetchone()[0])

# %% Step 9: What changed
type Snapshot = dict[str, tuple[int, bool]]  # url: (cents, stock)
type Change = tuple[str, str, str]          # (kind, url, details)


def snapshot(conn: sqlite3.Connection, day: str) -> Snapshot:
    rows = conn.execute("SELECT url, cents, in_stock FROM prices "
                        "WHERE seen_on = ?", (day,))
    return {url: (cents, bool(stock)) for url, cents, stock in rows}

# %% Step 9: What changed
def changes(before: Snapshot, after: Snapshot) -> Iterator[Change]:
    """Yield (kind, url, details) for everything that changed."""
    for url in after.keys() - before.keys():
        yield "NEW", url, money(after[url][0])
    for url in before.keys() - after.keys():
        yield "GONE", url, ""
    for url in after.keys() & before.keys():
        (was, had), (now, has) = before[url], after[url]
        if now != was:
            kind = "DROP" if now < was else "RISE"
            change = f"{money(was)} -> {money(now)}"
            yield kind, url, f"{change} ({(now - was) / was:+.0%})"
        if had != has:
            yield "BACK" if has else "SOLD OUT", url, ""

# %% Step 9: What changed
def report(conn: sqlite3.Connection) -> None:
    days = [d for (d,) in conn.execute(
        "SELECT DISTINCT seen_on FROM prices ORDER BY seen_on DESC "
        "LIMIT 2")]
    if len(days) < 2:
        print("Only one scrape so far: nothing to compare yet.")
        return
    new, old = days
    titles = dict(conn.execute("SELECT url, title FROM books"))
    found = sorted(changes(snapshot(conn, old), snapshot(conn, new)),
                   key=lambda change: (change[0], titles[change[1]]))
    print(f"Changes from {old} to {new}:")
    for kind, url, details in found:
        print(f"  {kind:<9} {titles[url]:<22} {details}".rstrip())
    if not found:
        print("  none")

# %% Step 9: What changed
report(conn)
conn.close()
