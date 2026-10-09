"""Solutions to the Chapter 20 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch20_solutions.py

The explanations are in ch20_solutions.md."""

# %% Exercise 20.1
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""CREATE TABLE planets (
    name TEXT PRIMARY KEY, distance REAL NOT NULL,
    moons INTEGER NOT NULL DEFAULT 0)""")
conn.executemany("INSERT INTO planets VALUES (?, ?, ?)",
                 [("Mercury", 0.39, 0), ("Venus", 0.72, 0),
                  ("Earth", 1.00, 1), ("Mars", 1.52, 2)])
sql = """SELECT name, moons FROM planets
         WHERE moons > 0 ORDER BY distance DESC"""
for name, moons in conn.execute(sql):
    print(f"{name:<6}{moons}")
conn.close()

# %% Exercise 20.2
BOOKS = [
    ("Dune", "Frank Herbert", 1965, 9.99, 4),
    ("Emma", "Jane Austen", 1815, 6.50, 2),
    ("Persuasion", "Jane Austen", 1817, 5.99, 0),
    ("The Hobbit", "J. R. R. Tolkien", 1937, 8.75, 5),
    ("Frankenstein", "Mary Shelley", 1818, 4.99, 3),
    ("Neuromancer", "William Gibson", 1984, 10.50, 1),
    ("Pride and Prejudice", "Jane Austen", 1813, 6.25, 6),
]

# %% Exercise 20.2
def book_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE books (
        id INTEGER PRIMARY KEY, title TEXT NOT NULL UNIQUE,
        author TEXT NOT NULL, year INTEGER,
        price REAL NOT NULL CHECK (price >= 0),
        stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0))""")
    conn.executemany("INSERT INTO books (title, author, year, price, "
                     "stock) VALUES (?, ?, ?, ?, ?)", BOOKS)
    conn.commit()
    return conn

# %% Exercise 20.2
conn = book_db()
row = conn.execute("SELECT MIN(price) AS low, MAX(price) AS high "
                   "FROM books").fetchone()
print(row["low"], row["high"])
count = conn.execute("SELECT COUNT(*) FROM books WHERE title LIKE ?",
                     ("%o%",)).fetchone()[0]
print(count, "titles contain an o")

# %% Exercise 20.3
def restock(conn, title, copies):
    if copies <= 0:
        raise ValueError(f"copies must be positive, not {copies}")
    with conn:
        cur = conn.execute("UPDATE books SET stock = stock + ? "
                           "WHERE title = ?", (copies, title))
    return cur.rowcount == 1

print(restock(conn, "Persuasion", 3))
print(restock(conn, "Ulysses", 3))
try:
    restock(conn, "Dune", 0)
except ValueError as error:
    print("Error:", error)
print(conn.execute("SELECT stock FROM books WHERE title = ?",
                   ("Persuasion",)).fetchone()[0])

# %% Exercise 20.4
def search(conn, text):
    sql = """SELECT title FROM books WHERE title LIKE ?
             ORDER BY title"""
    return [row["title"] for row in conn.execute(sql, (f"%{text}%",))]

print(search(conn, "an"))
print(search(conn, "PRIDE"))
print(search(conn, "' OR '1'='1"))

# %% Exercise 20.5
from datetime import date

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY, title TEXT NOT NULL UNIQUE,
    price REAL NOT NULL CHECK (price >= 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0));
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books (id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    sold_on TEXT NOT NULL);
"""

# %% Exercise 20.5
def open_shop(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn

# %% Exercise 20.5
def sell(conn, title, quantity, day):
    with conn:
        row = conn.execute("SELECT id FROM books WHERE title = ?",
                           (title,)).fetchone()
        if row is None:
            raise ValueError(f"no such book: {title}")
        conn.execute("UPDATE books SET stock = stock - ? "
                     "WHERE id = ?", (quantity, row["id"]))
        conn.execute("INSERT INTO sales (book_id, quantity, sold_on) "
                     "VALUES (?, ?, ?)",
                     (row["id"], quantity, day.isoformat()))

# %% Exercise 20.5
def sales_between(conn, first, last):
    sql = """SELECT s.sold_on, b.title, s.quantity
             FROM sales AS s JOIN books AS b ON s.book_id = b.id
             WHERE s.sold_on BETWEEN ? AND ?
             ORDER BY s.sold_on, b.title"""
    rows = conn.execute(sql, (first.isoformat(), last.isoformat()))
    return [(date.fromisoformat(r["sold_on"]), r["title"],
             r["quantity"]) for r in rows]

# %% Exercise 20.5
shop = open_shop(":memory:")
with shop:
    shop.executemany("INSERT INTO books (title, price, stock) "
                     "VALUES (?, ?, ?)", [("Dune", 9.99, 4),
                     ("Emma", 6.50, 2), ("The Hobbit", 8.75, 5)])
sell(shop, "Dune", 2, date(2026, 10, 1))
sell(shop, "The Hobbit", 1, date(2026, 10, 2))
sell(shop, "Emma", 1, date(2026, 10, 3))
sell(shop, "Dune", 1, date(2026, 10, 5))
for day, title, quantity in sales_between(
        shop, date(2026, 10, 2), date(2026, 10, 3)):
    print(day.strftime("%a %d %b"), title, quantity)

# %% Exercise 20.6
CUSTOMERS = """
CREATE TABLE customers (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE);
ALTER TABLE sales ADD COLUMN customer_id
    INTEGER REFERENCES customers (id);
"""
shop.executescript(CUSTOMERS)
with shop:
    shop.executemany("INSERT INTO customers (name, email) "
                     "VALUES (?, ?)", [("Ada", "ada@example.com"),
                     ("Grace", "grace@example.com"),
                     ("Linus", "linus@example.com")])
    shop.execute("UPDATE sales SET customer_id = 1 "
                 "WHERE id IN (1, 3)")
    shop.execute("UPDATE sales SET customer_id = 2 WHERE id = 2")

# %% Exercise 20.6
sql = """SELECT c.name, COALESCE(SUM(s.quantity), 0) AS copies
         FROM customers AS c LEFT JOIN sales AS s
              ON s.customer_id = c.id
         GROUP BY c.id ORDER BY copies DESC, c.name"""
for row in shop.execute(sql):
    print(f"{row['name']:<6}{row['copies']}")
try:
    with shop:
        shop.execute("INSERT INTO customers (name, email) "
                     "VALUES ('Ada L.', 'ada@example.com')")
except sqlite3.IntegrityError as error:
    print(error)
shop.close()
