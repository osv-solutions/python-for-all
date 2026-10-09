"""The practice server of Chapter 19: a small book API and web page.

Run it in a terminal of its own and leave it running while you try the
chapter's examples and exercises; press Ctrl+C to stop it:

    python practice_server.py

It listens only on your own computer, at http://127.0.0.1:8019.
"""
import json
import threading
import time
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
    """Send a response: a status line, headers, a blank line, a body."""
    text = json.dumps(body) if kind == "application/json" else body
    data = text.encode("utf-8")
    h.send_response(status)
    h.send_header("Content-Type", kind)
    h.send_header("Content-Length", str(len(data)))
    for name, value in (headers or {}).items():
        h.send_header(name, value)
    h.end_headers()
    h.wfile.write(data)


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


def start(port=8019):
    """Start the server in a background thread and return it."""
    server = ThreadingHTTPServer(("127.0.0.1", port), PracticeHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8019), PracticeHandler)
    print("Practice server at http://127.0.0.1:8019 (Ctrl+C stops it)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopped.")
