"""The practice sites of Project 11: a few web pages that misbehave.

Run it in a terminal of its own and leave it running while you try the
uptime checker; press Ctrl+C to stop it:

    python practice_server.py

It listens only on your own computer, at http://127.0.0.1:8111.
"""
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class PracticeSites(BaseHTTPRequestHandler):
    health_hits = 0          # requests to /api/health so far

    def do_GET(self):
        if self.path == "/":
            self.answer(200, "Welcome to the practice shop!")
        elif self.path == "/shop":
            time.sleep(0.8)                  # a slow page
            self.answer(200, "Our products")
        elif self.path == "/api/health":     # down 3 times out of 6
            n = PracticeSites.health_hits
            PracticeSites.health_hits += 1
            if (n // 3) % 2 == 1:
                self.answer(503, "Down for maintenance")
            else:
                self.answer(200, "OK")
        elif self.path == "/old":            # moved to the home page
            self.send_response(301)
            self.send_header("Location", "/")
            self.send_header("Content-Length", "0")
            self.end_headers()
        elif self.path == "/hang":           # never answers in time
            time.sleep(3)
            self.answer(200, "Sorry, I was busy")
        else:
            self.answer(404, "No such page")

    def answer(self, status, text):
        data = text.encode("utf-8")
        try:
            self.send_response(status)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except OSError:          # the client gave up waiting
            pass

    def log_message(self, *args):
        pass                     # keep the terminal quiet


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8111), PracticeSites)
    print("Practice sites at http://127.0.0.1:8111 (Ctrl+C stops)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
