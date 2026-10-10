"""Quick checks that the practice server answers as Chapter 19 describes.
Run from this folder with: python -m pytest"""
import pytest
import requests

import practice_server


@pytest.fixture(scope="module")
def base():
    server = practice_server.start(port=0)     # 0: any free port
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()
    server.server_close()


def test_list_and_detail(base):
    books = requests.get(f"{base}/api/books", timeout=5).json()
    assert len(books) == 5
    r = requests.get(f"{base}/api/books/3", timeout=5)
    assert r.json()["title"] == "Holes"


def test_unknown_book_is_404(base):
    r = requests.get(f"{base}/api/books/99", timeout=5)
    assert r.status_code == 404


def test_key_is_required(base):
    url = f"{base}/api/stats"
    assert requests.get(url, timeout=5).status_code == 401
    key = {"X-API-Key": practice_server.API_KEY}
    assert requests.get(url, headers=key, timeout=5).status_code == 200


def test_robots_and_page(base):
    assert "Disallow: /private/" in requests.get(
        f"{base}/robots.txt", timeout=5).text
    assert '<table id="top">' in requests.get(
        f"{base}/bestsellers.html", timeout=5).text


def test_book_pages(base):
    r = requests.get(f"{base}/books/2.html", timeout=5)
    assert '<span class="author">Frank Herbert</span>' in r.text
    r = requests.get(f"{base}/books/99.html", timeout=5)
    assert r.status_code == 404
