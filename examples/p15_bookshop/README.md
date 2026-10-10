# Project 15: Price Watch

`scraper.py` is the finished price watcher of Project 15: it scrapes every
page of a bookshop's catalog with Beautiful Soup, stores the prices in
SQLite and reports what changed since the last run. `practice_server.py` is
the practice bookshop it scrapes, *Classic Pages*, which uses only the
standard library and listens only on your own computer.

Start the shop in a terminal of its own and leave it running:

```bash
cd examples/p15_bookshop
python practice_server.py            # this week's prices
```

Then, in a second terminal with the book's virtual environment active
(`requests` and `beautifulsoup4` from `requirements.txt`):

```bash
python scraper.py --date 2026-10-05
```

To see a week go by, stop the shop with Ctrl+C, start it again with
`python practice_server.py --week 2`, and run
`python scraper.py --date 2026-10-12`. The prices are kept in `prices.db`;
delete it to start over.

The shop's `robots.txt` asks for a Crawl-delay of one second, so the first
scrape takes about 18 seconds.

`test_scraper.py` checks the parsing, the crawl and a two-week story with
`pytest` (`python -m pytest`).
