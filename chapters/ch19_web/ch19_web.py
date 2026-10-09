"""Chapter 19: Talking to the Web: HTTP and APIs

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch19_web.py

or open the notebook and run the cells in order.
"""

# %% 19.2 A practice server on your own computer
# Setup: recreates the context this solution builds on (not printed in the book).
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

# %% 19.2 A practice server on your own computer
# Setup: recreates the context this solution builds on (not printed in the book).
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

# %% 19.2 A practice server on your own computer
# Setup: recreates the context this solution builds on (not printed in the book).
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

server = ThreadingHTTPServer(("127.0.0.1", 8019), PracticeHandler)
threading.Thread(target=server.serve_forever, daemon=True).start()

# %% 19.2 A practice server on your own computer
BASE = "http://127.0.0.1:8019"

# %% 19.3 Your first request with requests
import requests

r = requests.get(f"{BASE}/api/books/3", timeout=5)
print(r.status_code, r.reason)
print(r.headers["Content-Type"])
print(r.text)

# %% 19.3 Your first request with requests
book = r.json()
print(type(book).__name__, book["title"], book["year"])

# %% 19.4 Query strings with params
options = {"author": "Jane Austen", "limit": 1}
r = requests.get(f"{BASE}/api/books", params=options, timeout=5)
print(r.url)
for book in r.json():
    print(book["id"], book["title"])

# %% 19.4 Query strings with params
r = requests.get(f"{BASE}/api/books/9", timeout=5)
print(r.status_code, r.reason)
print(r.json())

# %% 19.5 When things go wrong
def get_book(book_id):
    r = requests.get(f"{BASE}/api/books/{book_id}", timeout=5)
    r.raise_for_status()
    return r.json()

for book_id in [2, 9]:
    try:
        print(get_book(book_id)["title"])
    except requests.HTTPError as err:
        print(err)

# %% 19.5 When things go wrong
try:
    requests.get(f"{BASE}/api/slow", timeout=0.3)
except requests.Timeout:
    print("The server took too long; try again later.")

try:
    requests.get("http://no-such-host.invalid/", timeout=5)
except requests.ConnectionError:
    print("Could not connect to the server.")

# %% 19.6 Sending data with POST
new = {"title": "Matilda", "author": "Roald Dahl", "year": 1988}
r = requests.post(f"{BASE}/api/books", json=new, timeout=5)
print(r.status_code, r.reason)
print(r.headers["Location"])
print(r.json())

# %% 19.6 Sending data with POST
r = requests.post(f"{BASE}/api/books", json={"title": "Matilda"},
                  timeout=5)
print(r.status_code, r.json()["error"])

# %% 19.6 Sending data with POST
r = requests.get(f"{BASE}/old/books", timeout=5)
print(r.status_code, r.url)
print([step.status_code for step in r.history], len(r.json()))

# %% 19.7 Headers and the User-Agent
r = requests.get(f"{BASE}/api/echo", timeout=5)
for name, value in r.json()["headers"].items():
    print(f"{name}: {value}")

# %% 19.7 Headers and the User-Agent
agent = {"User-Agent": "ada-book-tool/1.0 (ada@example.com)"}
r = requests.get(f"{BASE}/api/echo", headers=agent, timeout=5)
print(r.json()["headers"]["User-Agent"])

# %% 19.7 Headers and the User-Agent
with requests.Session() as session:
    session.headers.update(agent)
    for book_id in [1, 4]:
        r = session.get(f"{BASE}/api/books/{book_id}", timeout=5)
        print(r.json()["title"])

# %% 19.8 A real API: the Python Package Index
url = "https://pypi.org/pypi/ruff/json"
r = requests.get(url, timeout=10)
r.raise_for_status()
info = r.json()["info"]
print(info["name"], "|", info["license_expression"])
print(info["summary"])
print(info["project_urls"]["Documentation"])

# %% 19.8 A real API: the Python Package Index
r = requests.get("https://pypi.org/pypi/no-such-package-zz/json",
                 timeout=10)
print(r.status_code, r.json())

# %% 19.9 API keys
r = requests.get(f"{BASE}/api/stats", timeout=5)
print(r.status_code, r.json())

# %% 19.9 API keys
import os

os.environ["BOOKS_API_KEY"] = "practice-key-123"   # as if exported

key = os.environ.get("BOOKS_API_KEY")
if key is None:
    raise SystemExit("Please set BOOKS_API_KEY first.")
r = requests.get(f"{BASE}/api/stats", headers={"X-API-Key": key},
                 timeout=5)
print(r.status_code, r.json())

# %% 19.10 Being polite
r = requests.get(f"{BASE}/api/popular", timeout=5)
print(r.status_code, r.reason, "| Retry-After:",
      r.headers["Retry-After"])

# %% 19.10 Being polite
import time

def get_politely(url, tries=4):
    for attempt in range(1, tries + 1):
        r = requests.get(url, timeout=5)
        if r.status_code != 429:
            r.raise_for_status()
            return r.json()
        wait = int(r.headers.get("Retry-After", 1))
        print(f"Attempt {attempt}: 429, waiting {wait} s")
        time.sleep(wait)
    raise RuntimeError(f"still too busy after {tries} tries")

print(get_politely(f"{BASE}/api/popular"))

# %% 19.10 Being polite
cache = {}

def get_book_cached(book_id):
    if book_id not in cache:
        print("fetching", book_id)
        cache[book_id] = get_book(book_id)
        time.sleep(0.2)                # a pause between requests
    return cache[book_id]

titles = [get_book_cached(i)["title"] for i in [1, 2, 1, 1, 2]]
print(titles)

# %% 19.11 Scraping web pages politely
print(requests.get(f"{BASE}/robots.txt", timeout=5).text)

# %% 19.11 Scraping web pages politely
from urllib.robotparser import RobotFileParser

robots = RobotFileParser(f"{BASE}/robots.txt")
robots.read()
for path in ["/bestsellers.html", "/private/staff.html"]:
    print(path, robots.can_fetch("ada-book-tool", f"{BASE}{path}"))

# %% 19.11 Scraping web pages politely
from html.parser import HTMLParser

html = requests.get(f"{BASE}/bestsellers.html", timeout=5).text
print(html.splitlines()[4])

# %% 19.11 Scraping web pages politely
class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.in_cell = [], False

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.rows.append([])       # a new row begins
        self.in_cell = tag in ("td", "th")

    def handle_endtag(self, tag):
        self.in_cell = False

    def handle_data(self, data):
        if self.in_cell:
            self.rows[-1].append(data)

# %% 19.11 Scraping web pages politely
parser = TableParser()
parser.feed(html)
header, *rows = parser.rows
print(header)
for rank, title, loans in rows:
    print(f"{rank}. {title:<6} {int(loans):>3} loans")

# %% 19.12 Under the hood: urllib.request
import json
from urllib.request import urlopen

with urlopen(f"{BASE}/api/books/5", timeout=5) as response:
    print(response.status, response.headers["Content-Type"])
    book = json.loads(response.read().decode("utf-8"))
print(book["title"], "by", book["author"])

# %% 19.12 Under the hood: urllib.request
# Setup: recreates the context this solution builds on (not printed in the book).
server.shutdown()
server.server_close()
