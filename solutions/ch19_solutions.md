# Solutions: Chapter 19, Talking to the Web: HTTP and APIs

Worked solutions to the exercises at the end of Chapter 19 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch19_solutions.ipynb`](ch19_solutions.ipynb) or the script `ch19_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

These solutions talk to a copy of the chapter's practice server, which the setup code below starts on port 8919, so that they can run while the chapter's own server is running on port 8019. When you try them with `examples/ch19_web/practice_server.py` running, write `http://127.0.0.1:8019` instead. The server keeps its books in memory, and the solutions run in order, so the books added in Exercise 19.4 are still there in Exercise 19.6.

<details>
<summary>Setup code: recreates the data and helpers from the chapter (click to show)</summary>

```python
import json, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

BOOKS = [
    {"id": 1, "title": "Emma", "author": "Jane Austen", "year": 1815},
    {"id": 2, "title": "Dune", "author": "Frank Herbert", "year": 1965},
    {"id": 3, "title": "Holes", "author": "Louis Sachar", "year": 1998},
    {"id": 4, "title": "Persuasion", "author": "Jane Austen",
     "year": 1817},
    {"id": 5, "title": "The Hobbit", "author": "J. R. R. Tolkien",
     "year": 1937},
]
API_KEY = "practice-key-123"
busy = {"count": 0}

def send(h, status, body, kind="application/json", headers=None):
    text = json.dumps(body) if kind == "application/json" else body
    data = text.encode("utf-8")
    h.send_response(status)
    h.send_header("Content-Type", kind)
    h.send_header("Content-Length", str(len(data)))
    for name, value in (headers or {}).items():
        h.send_header(name, value)
    h.end_headers()
    h.wfile.write(data)
```

</details>

<details>
<summary>Setup code: recreates the data and helpers from the chapter (click to show)</summary>

```python
def list_books(h, _):
    author = h.query.get("author")
    found = [b for b in BOOKS if author in (None, b["author"])]
    send(h, 200, found[:int(h.query.get("limit", len(found)))])

def one_book(h, book_id):
    for book in BOOKS:
        if str(book["id"]) == book_id:
            return send(h, 200, book)
    send(h, 404, {"error": f"no book with id {book_id}"})

def add_book(h, _):
    size = int(h.headers.get("Content-Length", 0))
    new = json.loads(h.rfile.read(size) or b"{}")
    if not new.get("title") or not new.get("author"):
        return send(h, 400, {"error": "title and author are required"})
    new = {"id": max(b["id"] for b in BOOKS) + 1} | new
    BOOKS.append(new)
    send(h, 201, new, headers={"Location": f"/api/books/{new['id']}"})

def stats(h, _):
    if h.headers.get("X-API-Key") != API_KEY:
        return send(h, 401, {"error": "missing or wrong API key"})
    authors = {b["author"] for b in BOOKS}
    send(h, 200, {"books": len(BOOKS), "authors": len(authors)})

def popular(h, _):
    busy["count"] += 1
    if busy["count"] % 3:              # turns away 2 requests out of 3
        return send(h, 429, {"error": "too many requests"},
                    headers={"Retry-After": "1"})
    send(h, 200, {"most_borrowed": "Dune", "loans": 41})

def slow(h, _):
    time.sleep(1)                      # a server that takes its time
    send(h, 200, {"done": True})

def echo(h, _):
    send(h, 200, {"method": h.command, "headers": dict(h.headers)})

def moved(h, _):
    send(h, 301, {"moved_to": "/api/books"},
         headers={"Location": "/api/books"})

def not_found(h, _):
    send(h, 404, {"error": "no such page"})
```

</details>

<details>
<summary>Setup code: recreates the data and helpers from the chapter (click to show)</summary>

```python
TEXT, HTML = "text/plain; charset=utf-8", "text/html; charset=utf-8"
ROBOTS = "User-agent: *\nDisallow: /private/\n"
PAGE = """<html><head><title>Bestsellers</title></head><body>
<h1>This week's bestsellers</h1>
<table id="top">
  <tr><th>Rank</th><th>Title</th><th>Loans</th></tr>
"""
for rank, (book_id, loans) in enumerate([(2, 41), (1, 35), (3, 28)], 1):
    title = BOOKS[book_id - 1]["title"]
    PAGE += f"""  <tr class="book">
    <td>{rank}</td>
    <td class="title"><a href="/books/{book_id}.html">{title}</a></td>
    <td class="loans">{loans}</td>
  </tr>
"""
PAGE += """</table>
<p class="nav"><a href="/api/books">All books</a> |
<a href="/private/staff.html">Staff only</a></p>
</body></html>"""

def book_page(h, name):
    for book in BOOKS:
        if f"{book['id']}.html" == name:
            return send(h, 200, f"""<html><body>
<h1>{book['title']}</h1>
<p>By <span class="author">{book['author']}</span>,
first published in <span class="year">{book['year']}</span>.</p>
<p><a href="/bestsellers.html">Back to the bestsellers</a></p>
</body></html>""", HTML)
    send(h, 404, "<h1>Not found</h1>", HTML)

GET_ROUTES = {
    "/api/books": list_books, "/api/books/<id>": one_book,
    "/api/stats": stats, "/api/popular": popular, "/api/slow": slow,
    "/api/echo": echo, "/old/books": moved,
    "/robots.txt": lambda h, _: send(h, 200, ROBOTS, TEXT),
    "/bestsellers.html": lambda h, _: send(h, 200, PAGE, HTML),
    "/books/<id>": book_page,
}
POST_ROUTES = {"/api/books": add_book}

class PracticeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.answer(GET_ROUTES)
    def do_POST(self):
        self.answer(POST_ROUTES)
    def answer(self, routes):
        url = urlsplit(self.path)
        self.query = {k: v[0] for k, v in parse_qs(url.query).items()}
        head, _, last = url.path.rpartition("/")
        route = routes.get(url.path) or routes.get(head + "/<id>")
        try:
            (route or not_found)(self, last)
        except (BrokenPipeError, ConnectionResetError):
            pass                       # the client stopped waiting
    def log_message(self, *args):
        pass                           # keep the terminal quiet

server = ThreadingHTTPServer(("127.0.0.1", 8919), PracticeHandler)
threading.Thread(target=server.serve_forever, daemon=True).start()
```

</details>

<details>
<summary>Setup code: recreates the data and helpers from the chapter (click to show)</summary>

```python
import os
import requests

BASE = "http://127.0.0.1:8919"
```

</details>

## Exercise 19.1

*Fetch the books by Jane Austen with `params=`, print the URL that `requests` built, then each book's title and year.*

```python
r = requests.get(f"{BASE}/api/books",
                 params={"author": "Jane Austen"}, timeout=5)
r.raise_for_status()
print(r.url)
for book in r.json():
    print(f"{book['title']} ({book['year']})")
```

Output:

```text
http://127.0.0.1:8919/api/books?author=Jane+Austen
Emma (1815)
Persuasion (1817)
```

`params=` turns the dictionary into the query string `?author=Jane+Austen`, with the space encoded as `+`. Without a `limit`, the server returns both of Jane Austen's books, Emma and Persuasion, as a list of dictionaries. `raise_for_status()` comes before `r.json()`, so an error response would raise an exception instead of being read as a list of books.

## Exercise 19.2

*For `requests`, `tabulate`, `pytest` and `no-such-package-zz`, print each package's name and summary from PyPI, or "not on PyPI" for a 404.*

```python
names = ["requests", "tabulate", "pytest", "no-such-package-zz"]
for name in names:
    r = requests.get(f"https://pypi.org/pypi/{name}/json", timeout=10)
    if r.status_code == 404:
        print(f"{name}: not on PyPI")
        continue
    r.raise_for_status()
    info = r.json()["info"]
    print(f"{info['name']}: {info['summary']}")
```

Output:

```text
requests: Python HTTP for Humans.
tabulate: Pretty-print tabular data
pytest: pytest: simple powerful testing with Python
no-such-package-zz: not on PyPI
```

These requests go to the real PyPI over the internet. The three real packages answer 200, and their `"info"` objects hold the name and the one-line summary that the package's authors wrote. The made-up name gets a 404, which the loop reports and skips with `continue` before `raise_for_status()` would turn it into an exception; any other error, such as a 503 from an overloaded server, would still raise. A polite version of this loop for many packages would add a short `time.sleep` between requests.

## Exercise 19.3

*Write `find_book(book_id)`: the book as a dictionary, `None` for a 404, and an exception for any other error.*

```python
def find_book(book_id):
    r = requests.get(f"{BASE}/api/books/{book_id}", timeout=5)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()

print(find_book(3))
print(find_book(99))
```

Output:

```text
{'id': 3, 'title': 'Holes', 'author': 'Louis Sachar', 'year': 1998}
None
```

The function checks for the one status code it wants to treat as normal, "no such book", before calling `raise_for_status()`, which takes care of everything else: a 500 or a 401 still raises a `requests.HTTPError`, and a server that can't be reached raises a `requests.ConnectionError`. Returning `None` for a missing book lets the caller write `if find_book(n) is None:` instead of a `try` statement, which suits a case that is expected to happen.

## Exercise 19.4

*Add two books with POST requests, print the status code and `Location` of each, count the books, then try to add a book without a title.*

```python
new_books = [
    {"title": "Matilda", "author": "Roald Dahl", "year": 1988},
    {"title": "Wonder", "author": "R. J. Palacio", "year": 2012},
]
for book in new_books:
    r = requests.post(f"{BASE}/api/books", json=book, timeout=5)
    print(r.status_code, r.reason, r.headers["Location"])

books = requests.get(f"{BASE}/api/books", timeout=5).json()
print(len(books), "books")
```

Output:

```text
201 Created /api/books/6
201 Created /api/books/7
7 books
```

Each POST is answered with 201 Created, and the `Location` header gives the new book's URL: the server numbered them 6 and 7, after the five books it started with. The list now holds seven books. Now a book without a title:

```python
r = requests.post(f"{BASE}/api/books", json={"author": "Anonymous"},
                  timeout=5)
print(r.status_code, r.reason)
print(r.json()["error"])
```

Output:

```text
400 Bad Request
title and author are required
```

The server refuses it with 400 Bad Request and explains why in the body. The book list is unchanged, still seven books.

## Exercise 19.5

*With Beautiful Soup, collect the links of the bestsellers page as full URLs and check each against `robots.txt`; then print each bestseller's title, author and year from its own page.*

```python
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup

page_url = f"{BASE}/bestsellers.html"
soup = BeautifulSoup(requests.get(page_url, timeout=5).text,
                     "html.parser")
robots = RobotFileParser(f"{BASE}/robots.txt")
robots.read()
for a in soup.select("a[href]"):
    url = urljoin(page_url, a["href"])
    allowed = robots.can_fetch("ada-book-tool", url)
    print(f"{a['href']:<20} {'allowed' if allowed else 'disallowed'}")
```

Output:

```text
/books/2.html        allowed
/books/1.html        allowed
/books/3.html        allowed
/api/books           allowed
/private/staff.html  disallowed
```

`select("a[href]")` finds only the `<a>` tags that have an `href`, so `a["href"]` can't fail. `urljoin` makes each link a complete URL before `can_fetch` checks it. The three book pages and the book list may be fetched; the staff page lies under `/private/`, which `robots.txt` asks automated clients to stay out of. Now the details of each bestseller:

```python
for a in soup.select("td.title a"):
    url = urljoin(page_url, a["href"])
    if not robots.can_fetch("ada-book-tool", url):
        continue
    book = BeautifulSoup(requests.get(url, timeout=5).text,
                         "html.parser")
    author = book.select_one(".author").get_text()
    year = int(book.select_one(".year").get_text())
    print(f"{book.h1.get_text():<6} {author:<14} {year}")
    time.sleep(0.2)
```

Output:

```text
Dune   Frank Herbert  1965
Emma   Jane Austen    1815
Holes  Louis Sachar   1998
```

Only the links inside the title cells lead to book pages. Each page is parsed into its own soup; `book.h1` is its heading, the title, and the classes `author` and `year` mark the other two values. The loop checks `robots.txt` before every request and pauses between them, as a polite scraper should.

## Exercise 19.6

*Write `BookClient`, with a session that sends your User-Agent and the API key from an environment variable, a base URL, a timeout, and the methods `book` (cached), `books` and `stats`.*

The key is read from the environment, as in the chapter, with one line standing in for the terminal command:

```python
os.environ["BOOKS_API_KEY"] = "practice-key-123"   # as if exported
AGENT = "ada-book-tool/1.0 (ada@example.com)"

def api_key():
    key = os.environ.get("BOOKS_API_KEY")
    if key is None:
        raise RuntimeError("Please set BOOKS_API_KEY first.")
    return key
```

The work is split between two classes (Chapter 13). `ApiClient` knows how to talk to any JSON API: it holds the session, the base URL and the timeout, and its `get` method checks every response:

```python
class ApiClient:
    """A session with a base URL, a timeout and error checking."""

    def __init__(self, base, headers, timeout=5):
        self.base, self.timeout = base, timeout
        self.session = requests.Session()
        self.session.headers.update(headers)

    def get(self, path, params=None):
        r = self.session.get(self.base + path, params=params,
                             timeout=self.timeout)
        r.raise_for_status()
        return r.json()
```

`BookClient` adds what is special about the book API: its key, its endpoints and a cache for single books:

```python
class BookClient(ApiClient):
    def __init__(self, base):
        headers = {"User-Agent": AGENT, "X-API-Key": api_key()}
        super().__init__(base, headers)
        self._cache = {}

    def book(self, book_id):
        if book_id not in self._cache:
            self._cache[book_id] = self.get(f"/api/books/{book_id}")
        return self._cache[book_id]

    def books(self, author=None):
        return self.get("/api/books", {"author": author})

    def stats(self):
        return self.get("/api/stats")
```

`requests` leaves out parameters whose value is `None`, so `books()` without an author asks for all books. Using the client:

```python
client = BookClient(BASE)
print(client.book(2)["title"], client.book(2) is client.book(2))
print([b["title"] for b in client.books("Jane Austen")])
print(client.stats())
try:
    client.book(42)
except requests.HTTPError as err:
    print("Error:", err.response.status_code)
```

Output:

```text
Dune True
['Emma', 'Persuasion']
{'books': 7, 'authors': 6}
Error: 404
```

`client.book(2)` is fetched once; the later calls return the very same dictionary from the cache, which `is` confirms. `stats()` succeeds because the session sends the key with every request: seven books, by six authors, after Exercise 19.4. A missing book raises an `HTTPError`, whose `response` attribute holds the response that caused it, so the caller can look at the status code. Because the client never puts the key in the code and always uses a timeout, it is safe to share.

## Exercise 19.7

*Change `get_politely` so that it waits at most `max_wait` seconds in total and uses exponential backoff when a 429 has no `Retry-After` header.*

Working out the wait is a small function of its own, which makes it easy to check:

```python
import time

def wait_time(r, attempt):
    """Seconds to wait after a 429: Retry-After, or 1, 2, 4..."""
    if "Retry-After" in r.headers:
        return int(r.headers["Retry-After"])
    return 2 ** (attempt - 1)

no_hint = requests.Response()
no_hint.status_code = 429
print([wait_time(no_hint, attempt) for attempt in range(1, 6)])
```

Output:

```text
[1, 2, 4, 8, 16]
```

The practice server always sends `Retry-After`, so the check builds a response by hand: `requests.Response()` creates an empty one with no headers, as a server that gives no hint would send. Without the header, the waits double: 1, 2, 4, 8 and 16 seconds. Now the retry loop, which keeps count of the time it has waited:

```python
def get_politely(url, tries=4, max_wait=5):
    waited = 0
    for attempt in range(1, tries + 1):
        r = requests.get(url, timeout=5)
        if r.status_code != 429:
            r.raise_for_status()
            return r.json()
        wait = wait_time(r, attempt)
        if waited + wait > max_wait:
            break
        print(f"Attempt {attempt}: 429, waiting {wait} s")
        time.sleep(wait)
        waited += wait
    raise RuntimeError(f"still too busy after waiting {waited} s")
```

Before each pause, the function checks whether the wait would take it past `max_wait`; if so, it gives up at once rather than sleeping first and failing afterward. Try it with the busy endpoint, which turns away two requests out of every three:

```python
url = f"{BASE}/api/popular"
print(get_politely(url))
try:
    print(get_politely(url, max_wait=1))
except RuntimeError as err:
    print(err)
```

Output:

```text
Attempt 1: 429, waiting 1 s
Attempt 2: 429, waiting 1 s
{'most_borrowed': 'Dune', 'loans': 41}
Attempt 1: 429, waiting 1 s
still too busy after waiting 1 s
```

The first call is refused twice, waits one second each time as `Retry-After` asks, and gets its answer at the third attempt. The second call, allowed to wait only one second in total, is refused once, waits, is refused again, and then gives up, because a second wait would exceed its limit.

<details>
<summary>Setup code: recreates the data and helpers from the chapter (click to show)</summary>

```python
server.shutdown()
server.server_close()
```

</details>
