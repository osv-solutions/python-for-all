"""Price watch: scrape a bookshop's catalog into SQLite and report changes.

Project 15 of Python for All. Start the practice shop first, in a terminal
of its own (python practice_server.py), then run:

    python scraper.py                    # scrape today, report changes
    python scraper.py --date 2026-10-12  # pretend that today is this day
"""
import argparse
import sqlite3
import time
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import date
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

BASE = "http://127.0.0.1:8115"
AGENT = "ada-price-watch/1.0 (ada@example.com)"


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


def make_fetcher(base: str, agent: str) -> Fetcher:
    robots = RobotFileParser(f"{base}/robots.txt")
    robots.read()
    session = requests.Session()
    session.headers["User-Agent"] = agent
    delay = robots.crawl_delay(agent) or 1
    return Fetcher(session, robots, agent, float(delay))


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


def parse_details(soup: BeautifulSoup) -> dict[str, str]:
    rows = soup.select("table.product_info tr")
    return {row.th.get_text(): row.td.get_text() for row in rows}


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


def open_db(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn


def add_book(conn: sqlite3.Connection, fetcher: Fetcher,
             item: Listing) -> None:
    info = parse_details(fetcher.soup(item.url))
    conn.execute("INSERT INTO books VALUES (?, ?, ?, ?)",
                 (item.url, item.title, info.get("Author"),
                  info.get("Category")))


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


type Snapshot = dict[str, tuple[int, bool]]  # url: (cents, stock)
type Change = tuple[str, str, str]          # (kind, url, details)


def snapshot(conn: sqlite3.Connection, day: str) -> Snapshot:
    rows = conn.execute("SELECT url, cents, in_stock FROM prices "
                        "WHERE seen_on = ?", (day,))
    return {url: (cents, bool(stock)) for url, cents, stock in rows}


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Watch prices.")
    parser.add_argument("--db", default="prices.db")
    parser.add_argument("--date", type=date.fromisoformat,
                        default=date.today(),
                        help="the day to record (default: today)")
    args = parser.parse_args()
    fetcher = make_fetcher(BASE, AGENT)
    conn = open_db(args.db)
    try:
        count = scrape(conn, fetcher, args.date)
        print(f"{args.date}: {count} books, {fetcher.count} requests")
        report(conn)
    except requests.RequestException as error:
        raise SystemExit(f"Scraping failed: {error}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
