"""The practice bookshop of Project 15: a small online shop to scrape.

Run it in a terminal of its own and leave it running while you try the
scraper; press Ctrl+C to stop it:

    python practice_server.py            # this week's prices
    python practice_server.py --week 2   # a week later: prices change

It listens only on your own computer, at http://127.0.0.1:8115.
"""
import argparse
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PER_PAGE = 6
ROBOTS = "User-agent: *\nDisallow: /checkout/\nCrawl-delay: 1\n"

# slug: (title, author, category, cents in week 1, stock in week 1)
BOOKS = {
    "moby-dick": ("Moby-Dick", "Herman Melville", "Adventure", 1299, 7),
    "pride-and-prejudice": ("Pride and Prejudice", "Jane Austen",
                            "Romance", 999, 12),
    "frankenstein": ("Frankenstein", "Mary Shelley", "Horror", 850, 2),
    "dracula": ("Dracula", "Bram Stoker", "Horror", 850, 5),
    "jane-eyre": ("Jane Eyre", "Charlotte Bronte", "Romance", 1000, 9),
    "the-time-machine": ("The Time Machine", "H. G. Wells",
                         "Science Fiction", 699, 4),
    "treasure-island": ("Treasure Island", "Robert Louis Stevenson",
                        "Adventure", 750, 6),
    "a-study-in-scarlet": ("A Study in Scarlet", "Arthur Conan Doyle",
                           "Mystery", 899, 3),
    "great-expectations": ("Great Expectations", "Charles Dickens",
                           "Classics", 1150, 8),
    "wuthering-heights": ("Wuthering Heights", "Emily Bronte",
                          "Romance", 925, 0),
    "the-war-of-the-worlds": ("The War of the Worlds", "H. G. Wells",
                              "Science Fiction", 799, 5),
    "kidnapped": ("Kidnapped", "Robert Louis Stevenson", "Adventure",
                  650, 1),
    "the-hound-of-the-baskervilles": ("The Hound of the Baskervilles",
                                      "Arthur Conan Doyle", "Mystery",
                                      975, 6),
    "middlemarch": ("Middlemarch", "George Eliot", "Classics", 1399, 2),
    "the-adventures-of-tom-sawyer": ("The Adventures of Tom Sawyer",
                                     "Mark Twain", "Adventure", 725, 10),
}

# What changes a week later: new prices and stock, a new book, a book gone
WEEK_2 = {
    "moby-dick": (999, 7),               # price drop
    "dracula": (675, 5),                 # price drop
    "jane-eyre": (1150, 9),              # price rise
    "frankenstein": (850, 0),            # sold out
    "wuthering-heights": (925, 4),       # back in stock
}
NEW_IN_WEEK_2 = {"the-call-of-the-wild": ("The Call of the Wild",
                                          "Jack London", "Adventure",
                                          599, 8)}
GONE_IN_WEEK_2 = {"kidnapped"}

state = {"week": 1}


def catalog():
    """The books on sale this week: {slug: (title, author, ...)}."""
    books = dict(BOOKS)
    if state["week"] >= 2:
        books |= NEW_IN_WEEK_2
        for slug in GONE_IN_WEEK_2:
            del books[slug]
        for slug, (cents, stock) in WEEK_2.items():
            title, author, category, _, _ = books[slug]
            books[slug] = (title, author, category, cents, stock)
    return dict(sorted(books.items(), key=lambda item: item[1][0]))


def money(cents):
    return f"${cents // 100}.{cents % 100:02d}"


def availability(stock, detail=False):
    if stock == 0:
        return '<p class="outofstock availability">Out of stock</p>'
    text = f"In stock ({stock} available)" if detail else "In stock"
    return f'<p class="instock availability">{text}</p>'


def short(title, size=20):
    return title if len(title) <= size else title[:size - 3] + "..."


def catalog_page(number):
    slugs = list(catalog())
    pages = (len(slugs) + PER_PAGE - 1) // PER_PAGE
    if not 1 <= number <= pages:
        return None
    items = []
    for slug in slugs[(number - 1) * PER_PAGE:number * PER_PAGE]:
        title, _, _, cents, stock = catalog()[slug]
        items.append(f"""<li><article class="product_pod">
  <h3><a href="books/{slug}.html" title="{title}">{short(title)}</a></h3>
  <p class="price_color">{money(cents)}</p>
  {availability(stock)}
</article></li>""")
    pager = f'<li class="current">Page {number} of {pages}</li>'
    if number < pages:
        pager += (f'<li class="next"><a href="page-{number + 1}.html">'
                  'next</a></li>')
    return f"""<html><head>
<title>Catalog, page {number} | Classic Pages</title>
</head><body>
<h1>All books</h1>
<ol class="row">
{chr(10).join(items)}
</ol>
<ul class="pager">{pager}</ul>
</body></html>"""


def book_page(slug):
    if slug not in catalog():
        return None
    title, author, category, cents, stock = catalog()[slug]
    return f"""<html><head><title>{title} | Classic Pages</title></head><body>
<ul class="breadcrumb"><li><a href="../page-1.html">Catalog</a></li>
<li>{category}</li></ul>
<h1>{title}</h1>
<p class="price_color">{money(cents)}</p>
{availability(stock, detail=True)}
<table class="product_info">
<tr><th>Author</th><td>{author}</td></tr>
<tr><th>Category</th><td>{category}</td></tr>
</table>
<p><a href="/checkout/add?book={slug}">Add to basket</a></p>
</body></html>"""


HOME = """<html><head><title>Classic Pages</title></head><body>
<h1>Classic Pages: old books, fair prices</h1>
<p><a href="catalogue/page-1.html">Browse the catalog</a></p>
</body></html>"""


class Shop(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            page = HOME
        elif path == "/robots.txt":
            return self.answer(200, ROBOTS, "text/plain")
        elif path.startswith("/catalogue/page-"):
            number = path.removeprefix("/catalogue/page-")
            number = number.removesuffix(".html")
            page = catalog_page(int(number)) if number.isdigit() else None
        elif path.startswith("/catalogue/books/"):
            slug = path.removeprefix("/catalogue/books/")
            page = book_page(slug.removesuffix(".html"))
        else:
            page = None
        if page is None:
            page = "<html><body><h1>Page not found</h1></body></html>"
            return self.answer(404, page)
        self.answer(200, page)

    def answer(self, status, text, kind="text/html"):
        data = text.encode("utf-8")
        try:
            self.send_response(status)
            self.send_header("Content-Type", f"{kind}; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except OSError:          # the client gave up waiting
            pass

    def log_message(self, *args):
        pass                     # keep the terminal quiet


def start(port=8115, week=1):
    """Start the shop in a background thread and return the server."""
    state["week"] = week
    server = ThreadingHTTPServer(("127.0.0.1", port), Shop)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def set_week(week):
    """Jump to another week: 1 is the first visit, 2 a week later."""
    state["week"] = week


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--week", type=int, choices=[1, 2], default=1)
    parser.add_argument("--port", type=int, default=8115)
    args = parser.parse_args()
    state["week"] = args.week
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Shop)
    print(f"Practice bookshop (week {args.week}) at "
          f"http://127.0.0.1:{args.port} (Ctrl+C stops it)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
