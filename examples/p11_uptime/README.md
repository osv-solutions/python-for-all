# Project 11: the practice sites

`practice_server.py` plays a handful of websites for the uptime checker of
Project 11. It uses only the standard library and listens only on your own
computer. Start it in a terminal of its own and leave it running:

```bash
cd examples/p11_uptime
python practice_server.py
```

Its address is `http://127.0.0.1:8111`; press Ctrl+C to stop it. The
project's script in `projects/` starts its own copy, so you don't need this
one to run that script.

| Page | What it does |
|---|---|
| `/` | Answers 200 at once |
| `/shop` | Answers 200 after 0.8 seconds (slow) |
| `/api/health` | Answers 200 three times, then 503 three times, and so on |
| `/old` | Redirects (301) to `/` |
| `/hang` | Waits 3 seconds, longer than the checker's timeout |
| anything else | 404 Not Found |

`sites.txt` lists these pages, plus `http://127.0.0.1:8119/`, where nothing
listens, to show a refused connection. Copy it next to your program and add
your own sites.
