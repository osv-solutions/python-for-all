"""Solutions to the Chapter 19 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch19_solutions.py

The explanations are in ch19_solutions.md."""

# %%
# Setup: recreates the context these solutions build on (from the chapter).
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

# %%
# Setup: recreates the context these solutions build on (from the chapter).
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

# %%
# Setup: recreates the context these solutions build on (from the chapter).
TEXT, HTML = "text/plain; charset=utf-8", "text/html; charset=utf-8"
ROBOTS = "User-agent: *\nDisallow: /private/\n"
PAGE = """<html><head><title>Bestsellers</title></head><body>
<h1>This week's bestsellers</h1>
<table>
  <tr><th>Rank</th><th>Title</th><th>Loans</th></tr>
  <tr><td>1</td><td>Dune</td><td>41</td></tr>
  <tr><td>2</td><td>Emma</td><td>35</td></tr>
  <tr><td>3</td><td>Holes</td><td>28</td></tr>
</table>
<p><a href="/api/books">All books</a> |
<a href="/private/staff.html">Staff only</a></p>
</body></html>"""

GET_ROUTES = {
    "/api/books": list_books, "/api/books/<id>": one_book,
    "/api/stats": stats, "/api/popular": popular, "/api/slow": slow,
    "/api/echo": echo, "/old/books": moved,
    "/robots.txt": lambda h, _: send(h, 200, ROBOTS, TEXT),
    "/bestsellers.html": lambda h, _: send(h, 200, PAGE, HTML),
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

# %%
# Setup: recreates the context these solutions build on (from the chapter).
import os
import requests

BASE = "http://127.0.0.1:8919"

# %% Exercise 19.1
r = requests.get(f"{BASE}/api/books",
                 params={"author": "Jane Austen"}, timeout=5)
r.raise_for_status()
print(r.url)
for book in r.json():
    print(f"{book['title']} ({book['year']})")

# %% Exercise 19.2
names = ["requests", "tabulate", "pytest", "no-such-package-zz"]
for name in names:
    r = requests.get(f"https://pypi.org/pypi/{name}/json", timeout=10)
    if r.status_code == 404:
        print(f"{name}: not on PyPI")
        continue
    r.raise_for_status()
    info = r.json()["info"]
    print(f"{info['name']}: {info['summary']}")

# %% Exercise 19.3
def find_book(book_id):
    r = requests.get(f"{BASE}/api/books/{book_id}", timeout=5)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()

print(find_book(3))
print(find_book(99))

# %% Exercise 19.4
new_books = [
    {"title": "Matilda", "author": "Roald Dahl", "year": 1988},
    {"title": "Wonder", "author": "R. J. Palacio", "year": 2012},
]
for book in new_books:
    r = requests.post(f"{BASE}/api/books", json=book, timeout=5)
    print(r.status_code, r.reason, r.headers["Location"])

books = requests.get(f"{BASE}/api/books", timeout=5).json()
print(len(books), "books")

# %% Exercise 19.4
r = requests.post(f"{BASE}/api/books", json={"author": "Anonymous"},
                  timeout=5)
print(r.status_code, r.reason)
print(r.json()["error"])

# %% Exercise 19.5
from html.parser import HTMLParser
from urllib.robotparser import RobotFileParser

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        href = dict(attrs).get("href")
        if tag == "a" and href:
            self.links.append(href)

# %% Exercise 19.5
html = requests.get(f"{BASE}/bestsellers.html", timeout=5).text
parser = LinkParser()
parser.feed(html)

robots = RobotFileParser(f"{BASE}/robots.txt")
robots.read()
for link in parser.links:
    allowed = robots.can_fetch("ada-book-tool", BASE + link)
    print(f"{link:<22} {'allowed' if allowed else 'disallowed'}")

# %% Exercise 19.6
os.environ["BOOKS_API_KEY"] = "practice-key-123"   # as if exported
AGENT = "ada-book-tool/1.0 (ada@example.com)"

def api_key():
    key = os.environ.get("BOOKS_API_KEY")
    if key is None:
        raise RuntimeError("Please set BOOKS_API_KEY first.")
    return key

# %% Exercise 19.6
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

# %% Exercise 19.6
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

# %% Exercise 19.6
client = BookClient(BASE)
print(client.book(2)["title"], client.book(2) is client.book(2))
print([b["title"] for b in client.books("Jane Austen")])
print(client.stats())
try:
    client.book(42)
except requests.HTTPError as err:
    print("Error:", err.response.status_code)

# %% Exercise 19.7
import time

def wait_time(r, attempt):
    """Seconds to wait after a 429: Retry-After, or 1, 2, 4..."""
    if "Retry-After" in r.headers:
        return int(r.headers["Retry-After"])
    return 2 ** (attempt - 1)

no_hint = requests.Response()
no_hint.status_code = 429
print([wait_time(no_hint, attempt) for attempt in range(1, 6)])

# %% Exercise 19.7
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

# %% Exercise 19.7
url = f"{BASE}/api/popular"
print(get_politely(url))
try:
    print(get_politely(url, max_wait=1))
except RuntimeError as err:
    print(err)

# %% Exercise 19.7
# Setup: recreates the context these solutions build on (from the chapter).
server.shutdown()
server.server_close()
