"""Tests for the price watch. Run from this folder: python -m pytest"""
from datetime import date

import pytest
from bs4 import BeautifulSoup

import practice_server
import scraper
from scraper import Listing, changes, crawl, parse_catalog, parse_price

PAGE = """<ol><li><article class="product_pod">
  <h3><a href="books/emma.html" title="Emma, a Novel">Emma, a...</a></h3>
  <p class="price_color">$7.05</p>
  <p class="outofstock availability">Out of stock</p>
</article></li></ol>"""


@pytest.mark.parametrize("text, cents", [
    ("$12.99", 1299), ("$5", 500), ("$0.5", 50), (" $1,000.00 ", None),
])
def test_parse_price(text, cents):
    if cents is None:
        with pytest.raises(ValueError):
            parse_price(text)
    else:
        assert parse_price(text) == cents


def test_parse_catalog_reads_one_listing():
    soup = BeautifulSoup(PAGE, "html.parser")
    url = "http://shop.test/catalogue/page-1.html"
    assert parse_catalog(soup, url) == [Listing(
        "http://shop.test/catalogue/books/emma.html", "Emma, a Novel",
        705, False)]


class FakeFetcher:
    """Serves pages from a dictionary instead of the network."""
    def __init__(self, pages):
        self.pages = pages

    def soup(self, url):
        return BeautifulSoup(self.pages[url], "html.parser")


def test_crawl_stops_at_a_loop():
    nxt = '<li class="next"><a href="{}">next</a></li>'
    pages = {"http://s.test/a": PAGE + nxt.format("b"),
             "http://s.test/b": PAGE + nxt.format("a")}
    found = list(crawl(FakeFetcher(pages), "http://s.test/a"))
    assert len(found) == 2


def test_changes_finds_every_kind():
    before = {"a": (1000, True), "b": (500, True), "c": (900, True)}
    after = {"a": (800, True), "b": (500, False), "d": (700, True)}
    found = sorted((kind, url) for kind, url, _ in changes(before, after))
    assert found == [("DROP", "a"), ("GONE", "c"), ("NEW", "d"),
                     ("SOLD OUT", "b")]


def test_two_weeks_against_the_practice_shop():
    server = practice_server.start(port=0)
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        fetcher = scraper.make_fetcher(base, scraper.AGENT)
        fetcher.delay = 0                # no need to wait in a test
        conn = scraper.open_db(":memory:")
        start = f"{base}/catalogue/page-1.html"
        assert scraper.scrape(conn, fetcher, date(2026, 10, 1),
                              start) == 15
        practice_server.set_week(2)
        assert scraper.scrape(conn, fetcher, date(2026, 10, 8),
                              start) == 15
        kinds = [k for k, _, _ in changes(
            scraper.snapshot(conn, "2026-10-01"),
            scraper.snapshot(conn, "2026-10-08"))]
        assert sorted(kinds) == ["BACK", "DROP", "DROP", "GONE", "NEW",
                                 "RISE", "SOLD OUT"]
    finally:
        practice_server.set_week(1)
        server.shutdown()
        server.server_close()

