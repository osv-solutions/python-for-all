"""Project 9 (Advanced): Library Management System with SQLite

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python p09_library.py

or open the notebook and run the cells in order.
"""

# %% Step 1: Plan the tables
"""A small library system: books, members and loans in SQLite."""
import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

LOAN_DAYS = 14          # how long a loan lasts
MAX_LOANS = 3           # loans a member may hold at once
FINE_PER_DAY = 0.25     # dollars for each day late

# %% Step 1: Plan the tables
SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY, isbn TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL, author TEXT NOT NULL, year INTEGER,
    copies INTEGER NOT NULL CHECK (copies > 0));
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE, joined TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books (id),
    member_id INTEGER NOT NULL REFERENCES members (id),
    borrowed TEXT NOT NULL, due TEXT NOT NULL,
    returned TEXT);                    -- NULL while on loan
CREATE VIEW IF NOT EXISTS open_loans AS
    SELECT * FROM loans WHERE returned IS NULL;
"""

# %% Step 2: Rows become objects
@dataclass
class Book:
    id: int
    isbn: str
    title: str
    author: str
    year: int
    copies: int


@dataclass
class Member:
    id: int
    name: str
    email: str
    joined: date

# %% Step 2: Rows become objects
@dataclass
class Loan:
    id: int
    book_id: int
    member_id: int
    borrowed: date
    due: date
    returned: date | None = None

    def days_late(self, today: date) -> int:
        """Days past the due date, up to the return or today."""
        end = self.returned or today
        return max(0, (end - self.due).days)

    def fine(self, today: date) -> float:
        return self.days_late(today) * FINE_PER_DAY

# %% Step 2: Rows become objects
loan = Loan(1, 1, 1, date(2026, 10, 1), date(2026, 10, 15))
for day in [date(2026, 10, 15), date(2026, 10, 20)]:
    print(day, loan.days_late(day), loan.fine(day))

# %% Step 2: Rows become objects
def with_dates(row: sqlite3.Row, *names: str) -> dict:
    """The row as a dictionary, with the named columns as dates."""
    values = dict(row)
    for name in names:
        if values[name] is not None:
            values[name] = date.fromisoformat(values[name])
    return values


def to_member(row: sqlite3.Row) -> Member:
    return Member(**with_dates(row, "joined"))


def to_loan(row: sqlite3.Row) -> Loan:
    return Loan(**with_dates(row, "borrowed", "due", "returned"))

# %% Step 3: Refusals are exceptions
class LibraryError(Exception):
    """A request that the library refuses."""


class NotFoundError(LibraryError):
    """No book, member or loan has the given id."""


class RuleError(LibraryError):
    """The lending rules don't allow the request."""

# %% Step 4: Opening the library
class Database:
    def __init__(self, path: str | Path = ":memory:") -> None:
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript(SCHEMA)

    def run(self, sql: str, *values: object) -> list[sqlite3.Row]:
        """Run one statement in a transaction and return its rows."""
        try:
            with self.conn:
                return self.conn.execute(sql, values).fetchall()
        except sqlite3.IntegrityError as error:
            raise LibraryError(f"refused: {error}") from error

    def close(self) -> None:
        self.conn.close()

# %% Step 4: Opening the library
class Catalog(Database):
    def add_book(self, isbn: str, title: str, author: str,
                 year: int, copies: int = 1) -> Book:
        rows = self.run(
            "INSERT INTO books (isbn, title, author, year, copies) "
            "VALUES (?, ?, ?, ?, ?) RETURNING *",
            isbn, title, author, year, copies)
        return Book(**rows[0])

    def add_member(self, name: str, email: str,
                   joined: date) -> Member:
        rows = self.run("INSERT INTO members (name, email, joined) "
                        "VALUES (?, ?, ?) RETURNING *",
                        name, email, joined.isoformat())
        return to_member(rows[0])

# %% Step 4: Opening the library
class Lookup(Catalog):
    def book(self, book_id: int) -> Book:
        rows = self.run("SELECT * FROM books WHERE id = ?", book_id)
        if not rows:
            raise NotFoundError(f"no book with id {book_id}")
        return Book(**rows[0])

    def member(self, member_id: int) -> Member:
        rows = self.run("SELECT * FROM members WHERE id = ?",
                        member_id)
        if not rows:
            raise NotFoundError(f"no member with id {member_id}")
        return to_member(rows[0])

# %% Step 4: Opening the library
Path("library.db").unlink(missing_ok=True)   # start fresh every run
shelf = Lookup("library.db")
for isbn, title, author, year, copies in [
        ("9780000000019", "Dune", "Frank Herbert", 1965, 2),
        ("9780000000026", "Emma", "Jane Austen", 1815, 1),
        ("9780000000033", "The Hobbit", "J. R. R. Tolkien", 1937, 2),
        ("9780000000040", "Frankenstein", "Mary Shelley", 1818, 1),
        ("9780000000057", "Persuasion", "Jane Austen", 1817, 1)]:
    shelf.add_book(isbn, title, author, year, copies)
for name, day in [("Ada", 1), ("Ravi", 15), ("Dina", 29)]:
    shelf.add_member(name, f"{name.lower()}@example.com",
                     date(2026, 9, day))
try:
    shelf.add_book("9780000000019", "Dune", "Frank Herbert", 1965)
except LibraryError as error:
    print(error)
shelf.close()

# %% Step 5: Borrowing by the rules
class Lending(Lookup):
    def borrow(self, book_id: int, member_id: int,
               today: date) -> Loan:
        book, member = self.book(book_id), self.member(member_id)
        out = self.run("SELECT COUNT(*) FROM open_loans "
                       "WHERE book_id = ?", book_id)[0][0]
        if out >= book.copies:
            raise RuleError(f"all copies of {book.title} are out")
        held = self.run("SELECT COUNT(*) FROM open_loans "
                        "WHERE member_id = ?", member_id)[0][0]
        if held >= MAX_LOANS:
            raise RuleError(f"{member.name} already has {held} loans")
        due = today + timedelta(days=LOAN_DAYS)
        return to_loan(self.run(
            "INSERT INTO loans (book_id, member_id, borrowed, due) "
            "VALUES (?, ?, ?, ?) RETURNING *", book_id, member_id,
            today.isoformat(), due.isoformat())[0])

# %% Step 6: Returns and fines
class Library(Lending):
    def give_back(self, loan_id: int, today: date) -> Loan:
        rows = self.run("SELECT returned FROM loans WHERE id = ?",
                        loan_id)
        if not rows:
            raise NotFoundError(f"no loan with id {loan_id}")
        if rows[0]["returned"] is not None:
            raise RuleError(f"loan {loan_id} was already returned")
        rows = self.run("UPDATE loans SET returned = ? WHERE id = ? "
                        "RETURNING *", today.isoformat(), loan_id)
        return to_loan(rows[0])

# %% Step 6: Returns and fines
lib = Library("library.db")
oct1, oct3 = date(2026, 10, 1), date(2026, 10, 3)
requests = [(1, 1, oct1), (2, 1, oct1), (1, 2, oct1), (1, 3, oct3),
            (3, 1, oct3), (4, 1, oct3), (4, 3, oct3)]
for book_id, member_id, day in requests:
    try:
        loan = lib.borrow(book_id, member_id, day)
        print(f"loan {loan.id}: book {book_id} to member "
              f"{member_id}, due {loan.due}")
    except LibraryError as error:
        print("refused:", error)

# %% Step 6: Returns and fines
returns = [(3, date(2026, 10, 12)), (2, date(2026, 10, 20)),
           (2, date(2026, 10, 21))]
for loan_id, day in returns:
    try:
        loan = lib.give_back(loan_id, day)
        print(f"loan {loan_id}: {loan.days_late(day)} days late, "
              f"fine ${loan.fine(day):.2f}")
    except LibraryError as error:
        print("refused:", error)

# %% Step 7: Search and reports
# Setup: recreates the context this solution builds on (not printed in the book).
def show(rows: list[sqlite3.Row]) -> None:
    """Print rows as a table, each column as wide as it needs."""
    if not rows:
        print("(none)")
        return
    table = [list(rows[0].keys())]
    table += [["-" if v is None else str(v) for v in r] for r in rows]
    widths = [max(len(cell) for cell in col) for col in zip(*table)]
    for line in table:
        cells = [cell.ljust(w) for cell, w in zip(line, widths)]
        print("  ".join(cells).rstrip())

# %% Step 7: Search and reports
def search(lib: Library, text: str) -> list[Book]:
    rows = lib.run("SELECT * FROM books WHERE title LIKE ?1 "
                   "OR author LIKE ?1 ORDER BY title", f"%{text}%")
    return [Book(**row) for row in rows]

# %% Step 7: Search and reports
oct20 = date(2026, 10, 20)
show(lib.run("SELECT * FROM open_loans"))
print([book.title for book in search(lib, "AUSTEN")])

# %% Step 7: Search and reports
def overdue(lib: Library, today: date) -> list[sqlite3.Row]:
    return lib.run("""
        SELECT l.id AS loan, b.title, m.name, l.due,
               CAST(julianday(?1) - julianday(l.due) AS INTEGER)
                   AS days,
               printf('$%.2f', (julianday(?1) - julianday(l.due))
                               * ?2) AS fine
        FROM open_loans AS l
        JOIN books AS b ON b.id = l.book_id
        JOIN members AS m ON m.id = l.member_id
        WHERE l.due < ?1 ORDER BY l.due, l.id""",
        today.isoformat(), FINE_PER_DAY)

# %% Step 7: Search and reports
def most_borrowed(lib: Library, top: int = 3) -> list[sqlite3.Row]:
    return lib.run("""
        SELECT b.title, COUNT(l.id) AS loans
        FROM books AS b LEFT JOIN loans AS l ON l.book_id = b.id
        GROUP BY b.id ORDER BY loans DESC, b.title LIMIT ?""", top)


def history(lib: Library, member_id: int) -> list[sqlite3.Row]:
    return lib.run("""
        SELECT b.title, l.borrowed, l.due, l.returned
        FROM loans AS l JOIN books AS b ON b.id = l.book_id
        WHERE l.member_id = ? ORDER BY l.borrowed, l.id""", member_id)

# %% Step 7: Search and reports
show(overdue(lib, oct20))
show(most_borrowed(lib))
show(history(lib, 1))
lib.close()
