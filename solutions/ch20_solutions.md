# Solutions: Chapter 20, Databases with SQLite

Worked solutions to the exercises at the end of Chapter 20 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch20_solutions.ipynb`](ch20_solutions.ipynb) or the script `ch20_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 20.1

*Create an in-memory table `planets`, add the four inner planets with `executemany`, and print the planets that have moons, farthest first.*

```python
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
```

Output:

```text
Mars  2
Earth 1
```

`name` is the primary key here, since a planet's name identifies it; `INTEGER PRIMARY KEY` isn't the only choice. `INSERT INTO planets VALUES (?, ?, ?)` leaves out the column list, which works when you give a value for every column, in the order of the `CREATE TABLE`. `WHERE moons > 0` drops Mercury and Venus, and `ORDER BY distance DESC` puts Mars (2 moons) before Earth (1). Unpacking each row into `name, moons` in the `for` line works because rows are plain tuples here. An in-memory database leaves no file behind.

## Exercise 20.2

*Print the lowest and highest price of the `books` table in one query, and count the titles that contain the letter "o".*

The solution rebuilds the chapter's seven books in memory, as they were before the price rise:

```python
BOOKS = [
    ("Dune", "Frank Herbert", 1965, 9.99, 4),
    ("Emma", "Jane Austen", 1815, 6.50, 2),
    ("Persuasion", "Jane Austen", 1817, 5.99, 0),
    ("The Hobbit", "J. R. R. Tolkien", 1937, 8.75, 5),
    ("Frankenstein", "Mary Shelley", 1818, 4.99, 3),
    ("Neuromancer", "William Gibson", 1984, 10.50, 1),
    ("Pride and Prejudice", "Jane Austen", 1813, 6.25, 6),
]
```

```python
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
```

```python
conn = book_db()
row = conn.execute("SELECT MIN(price) AS low, MAX(price) AS high "
                   "FROM books").fetchone()
print(row["low"], row["high"])
count = conn.execute("SELECT COUNT(*) FROM books WHERE title LIKE ?",
                     ("%o%",)).fetchone()[0]
print(count, "titles contain an o")
```

Output:

```text
4.99 10.5
3 titles contain an o
```

`MIN` and `MAX` are aggregates like `COUNT`, so one `SELECT` can compute both: the cheapest book costs $4.99 (*Frankenstein*) and the dearest $10.5 (*Neuromancer*; Python prints `10.5` without a trailing zero). `COUNT(*)` with `WHERE title LIKE '%o%'` counts 3 titles: *Persuasion*, *The Hobbit* and *Neuromancer*. Since `LIKE` ignores case, a title with a capital O would count too.

## Exercise 20.3

*Write `restock(conn, title, copies)`, which returns `True` if a book was changed and `False` if the title doesn't exist, and raises a `ValueError` for zero or negative copies.*

```python
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
```

Output:

```text
True
False
Error: copies must be positive, not 0
3
```

The check on `copies` comes first, so bad input never reaches the database. `stock = stock + ?` lets the database compute the new stock. `rowcount` is 1 when the `WHERE` matched a book and 0 when it matched nothing, so `cur.rowcount == 1` gives `True` for *Persuasion* and `False` for the unknown *Ulysses*; the `UNIQUE` title guarantees that it can never be more than 1. The `cur` variable is still usable after the `with` block, which only committed the change. *Persuasion* had 0 copies, so it now has 3.

## Exercise 20.4

*Write `search(conn, text)`, which returns the titles containing `text` in alphabetical order, using `LIKE` with a placeholder.*

```python
def search(conn, text):
    sql = """SELECT title FROM books WHERE title LIKE ?
             ORDER BY title"""
    return [row["title"] for row in conn.execute(sql, (f"%{text}%",))]

print(search(conn, "an"))
print(search(conn, "PRIDE"))
print(search(conn, "' OR '1'='1"))
```

Output:

```text
['Frankenstein', 'Neuromancer', 'Pride and Prejudice']
['Pride and Prejudice']
[]
```

The `%` signs are added to the value in Python, not to the SQL, so the whole pattern goes through the placeholder. "an" matches three titles, in alphabetical order thanks to `ORDER BY title`. "PRIDE" finds *Pride and Prejudice* because `LIKE` ignores case. The attack string is treated as plain text to search for, and no title contains it, so the result is an empty list. (A user could still type `%` or `_` to widen the search; that only affects which titles are found, never the SQL itself.)

## Exercise 20.5

*Write `sales_between(conn, first, last)` for the shop module, returning `(date, title, quantity)` tuples with real `date` objects.*

The shop module of the chapter, repeated so that this solution runs on its own:

```python
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
```

```python
def open_shop(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn
```

```python
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
```

The new function:

```python
def sales_between(conn, first, last):
    sql = """SELECT s.sold_on, b.title, s.quantity
             FROM sales AS s JOIN books AS b ON s.book_id = b.id
             WHERE s.sold_on BETWEEN ? AND ?
             ORDER BY s.sold_on, b.title"""
    rows = conn.execute(sql, (first.isoformat(), last.isoformat()))
    return [(date.fromisoformat(r["sold_on"]), r["title"],
             r["quantity"]) for r in rows]
```

```python
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
```

Output:

```text
Fri 02 Oct The Hobbit 1
Sat 03 Oct Emma 1
```

`sales_between` converts the two dates to ISO text for the query and converts each `sold_on` back with `date.fromisoformat`, so the caller sees only `date` objects and never the storage format. `BETWEEN` includes both ends, so the sales of October 2 and 3 are found (*The Hobbit* on Friday, *Emma* on Saturday), while those of October 1 and 5 are not. `strftime` works on the results because they are real dates. The shop here lives in memory (`":memory:"`), which suits a test.

## Exercise 20.6

*Add a `customers` table and an optional `customer_id` foreign key to `sales`, then list every customer with the number of copies bought.*

```python
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
```

```python
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
```

Output:

```text
Ada   3
Grace 1
Linus 0
UNIQUE constraint failed: customers.email
```

`ALTER TABLE ... ADD COLUMN` adds a column to an existing table; old rows get `NULL` in it, which here means "anonymous sale". The column has no `NOT NULL`, so `NULL` stays allowed, and the `REFERENCES` makes every non-`NULL` value point at a real customer. Sales 1 and 3 (2 copies of *Dune* and 1 of *Emma*) go to Ada and sale 2 to Grace; sale 4 stays anonymous. The `LEFT JOIN` starting from `customers` keeps Linus, who bought nothing, and `COALESCE` turns his `NULL` sum into 0: Ada 3, Grace 1, Linus 0. The last insert reuses Ada's email address, so the `UNIQUE` constraint refuses it with `UNIQUE constraint failed: customers.email`.
