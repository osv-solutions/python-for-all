# Chapter 19: the practice server

`practice_server.py` is the small book API and web page that the examples
and exercises of Chapter 19 talk to. It uses only the standard library and
listens only on your own computer. Start it in a terminal of its own and
leave it running:

```bash
cd examples/ch19_web
python practice_server.py
```

Its address is `http://127.0.0.1:8019`; press Ctrl+C to stop it. It keeps
its books in memory, so every restart begins again with the same five books.
The chapter's script in `chapters/` starts its own copy, so you don't need
this one to run that script.

| Endpoint | What it does |
|---|---|
| `GET /api/books` | All books; options `author=` and `limit=` |
| `GET /api/books/<id>` | One book, or 404 |
| `POST /api/books` | Adds a book (JSON with `title` and `author`): 201, or 400 |
| `GET /api/stats` | Needs the header `X-API-Key: practice-key-123`, else 401 |
| `GET /api/popular` | Turns away 2 requests out of 3 with 429 and `Retry-After` |
| `GET /api/slow` | Answers after one second, to try timeouts |
| `GET /api/echo` | Answers with the headers it received |
| `GET /old/books` | Redirects (301) to `/api/books` |
| `GET /robots.txt`, `/bestsellers.html` | A robots file and a web page to scrape |
| `GET /books/<id>.html` | A page for one book, linked from the bestsellers |

`test_practice_server.py` checks the server with `pytest` (`python -m pytest`).
