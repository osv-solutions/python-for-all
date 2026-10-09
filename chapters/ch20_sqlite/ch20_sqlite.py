"""Chapter 20: Databases with SQLite

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch20_sqlite.py

or open the notebook and run the cells in order.
"""

# %% 20.2 Your first database
import sqlite3
from pathlib import Path

Path("shop.db").unlink(missing_ok=True)    # start fresh every run
conn = sqlite3.connect("shop.db")
conn.execute("""
    CREATE TABLE books (
        id     INTEGER PRIMARY KEY,
        title  TEXT NOT NULL UNIQUE,
        author TEXT NOT NULL,
        year   INTEGER,
        price  REAL NOT NULL CHECK (price >= 0),
        stock  INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
    )
""")
print(type(conn).__name__, Path("shop.db").exists())

# %% 20.3 Adding rows
books = [
    ("Dune", "Frank Herbert", 1965, 9.99, 4),
    ("Emma", "Jane Austen", 1815, 6.50, 2),
    ("Persuasion", "Jane Austen", 1817, 5.99, 0),
    ("The Hobbit", "J. R. R. Tolkien", 1937, 8.75, 5),
    ("Frankenstein", "Mary Shelley", 1818, 4.99, 3),
    ("Neuromancer", "William Gibson", 1984, 10.50, 1),
    ("Pride and Prejudice", "Jane Austen", 1813, 6.25, 6),
]
conn.executemany(
    "INSERT INTO books (title, author, year, price, stock) "
    "VALUES (?, ?, ?, ?, ?)", books)
conn.commit()
print("rows:", conn.execute("SELECT COUNT(*) FROM books").fetchone())

# %% 20.4 Asking questions with SELECT
cur = conn.execute(
    "SELECT title, price FROM books WHERE price < ?", (7,))
for row in cur:
    print(row)

# %% 20.4 Asking questions with SELECT
sql = """SELECT title, year FROM books
         WHERE title LIKE ? AND stock > 0
         ORDER BY year DESC LIMIT 2"""
print(conn.execute(sql, ("%u%",)).fetchall())

# %% 20.4 Asking questions with SELECT
conn.row_factory = sqlite3.Row
row = conn.execute(
    "SELECT title, author, year, price FROM books WHERE id = ?",
    (2,)).fetchone()
print(row["author"], row["year"], row["price"])
print(dict(row))

# %% 20.5 Counting and summing
sql = """SELECT author, COUNT(*) AS titles, SUM(stock) AS copies,
                ROUND(AVG(price), 2) AS avg_price
         FROM books GROUP BY author ORDER BY titles DESC, author"""
for row in conn.execute(sql):
    print(f"{row['author']:<17}{row['titles']:>3}{row['copies']:>4}"
          f"{row['avg_price']:>7}")
having = sql.replace("ORDER BY", "HAVING COUNT(*) > 1 ORDER BY")
print([tuple(r) for r in conn.execute(having)])

# %% 20.6 Changing and deleting rows
cur = conn.execute(
    "UPDATE books SET price = ROUND(price * 1.10, 2) "
    "WHERE author = ?", ("Jane Austen",))
print("updated:", cur.rowcount)
cur = conn.execute("DELETE FROM books WHERE stock = 0")
print("deleted:", cur.rowcount)
conn.commit()

# %% 20.7 Keeping data safe: placeholders
def find_by_author_unsafe(name):
    sql = f"SELECT title FROM books WHERE author = '{name}'"
    return [row["title"] for row in conn.execute(sql)]

print(find_by_author_unsafe("Mary Shelley"))
print(", ".join(find_by_author_unsafe("nobody' OR '1'='1")))

# %% 20.7 Keeping data safe: placeholders
def find_by_author(name):
    sql = "SELECT title FROM books WHERE author = ?"
    return [row["title"] for row in conn.execute(sql, (name,))]

print(find_by_author("Mary Shelley"))
print(find_by_author("nobody' OR '1'='1"))
print(find_by_author("Flann O'Brien"))

# %% 20.7 Keeping data safe: placeholders
sql = """SELECT title, year, price FROM books
         WHERE year < :before AND price <= :max_price"""
limits = {"before": 1900, "max_price": 7.00}
for row in conn.execute(sql, limits):
    print(tuple(row))

# %% 20.8 Keeping data safe: transactions
changes = [("Dune", 3), ("Emma", 2), ("Neuromancer", -5)]
try:
    with conn:
        for title, change in changes:
            conn.execute("UPDATE books SET stock = stock + ? "
                         "WHERE title = ?", (change, title))
except sqlite3.IntegrityError as error:
    print("rolled back:", error)
sql = "SELECT title, stock FROM books WHERE title IN (?, ?, ?)"
titles = ("Dune", "Emma", "Neuromancer")
print([tuple(r) for r in conn.execute(sql, titles)])

# %% 20.8 Keeping data safe: transactions
from contextlib import closing

with closing(sqlite3.connect("shop.db")) as other:
    count = other.execute("SELECT COUNT(*) FROM books")
    print(count.fetchone()[0], "books")

# %% 20.9 Two tables and a foreign key
conn.execute("PRAGMA foreign_keys = ON")
conn.execute("""
    CREATE TABLE sales (
        id       INTEGER PRIMARY KEY,
        book_id  INTEGER NOT NULL REFERENCES books (id),
        quantity INTEGER NOT NULL CHECK (quantity > 0),
        sold_on  TEXT NOT NULL
    )
""")
print("sales table created")

# %% 20.9 Two tables and a foreign key
sales = [(1, 1, "2026-10-01"), (4, 2, "2026-10-01"),
         (2, 1, "2026-10-02"), (1, 2, "2026-10-03")]
with conn:
    conn.executemany("INSERT INTO sales (book_id, quantity, sold_on) "
                     "VALUES (?, ?, ?)", sales)
try:
    with conn:
        conn.execute("INSERT INTO sales (book_id, quantity, sold_on) "
                     "VALUES (99, 1, '2026-10-03')")
except sqlite3.IntegrityError as error:
    print(error)

# %% 20.9 Two tables and a foreign key
sql = """SELECT sales.sold_on, books.title, sales.quantity
         FROM sales JOIN books ON sales.book_id = books.id
         ORDER BY sales.sold_on, books.title"""
for row in conn.execute(sql):
    print(row["sold_on"], f"{row['title']:<12}", row["quantity"])

# %% 20.9 Two tables and a foreign key
sql = """SELECT books.title, COUNT(sales.id) AS sales,
                COALESCE(SUM(sales.quantity), 0) AS copies
         FROM books LEFT JOIN sales ON sales.book_id = books.id
         GROUP BY books.id ORDER BY copies DESC, books.title"""
for row in conn.execute(sql):
    print(f"{row['title']:<20}{row['sales']:>2}{row['copies']:>3}")

# %% 20.11 Putting it together: a shop module
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

# %% 20.11 Putting it together: a shop module
def open_shop(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn

# %% 20.11 Putting it together: a shop module
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

# %% 20.11 Putting it together: a shop module
from datetime import date

conn.close()                  # done with the experiments in shop.db
Path("bookshop.db").unlink(missing_ok=True)
shop = open_shop("bookshop.db")
with shop:
    shop.executemany("INSERT INTO books (title, price, stock) "
                     "VALUES (?, ?, ?)", [("Dune", 9.99, 4),
                     ("Emma", 6.50, 2), ("The Hobbit", 8.75, 5)])
sell(shop, "Dune", 2, date(2026, 10, 1))
sell(shop, "The Hobbit", 1, date(2026, 10, 2))
try:
    sell(shop, "Emma", 3, date(2026, 10, 2))
except sqlite3.IntegrityError as error:
    print("Sale refused:", error)

# %% 20.11 Putting it together: a shop module
sql = """SELECT b.title, b.stock, COUNT(s.id) AS sales
         FROM books AS b LEFT JOIN sales AS s
              ON s.book_id = b.id
         GROUP BY b.id ORDER BY b.title"""
for row in shop.execute(sql):
    print(f"{row['title']:<11} stock {row['stock']}, "
          f"sales {row['sales']}")
shop.close()
