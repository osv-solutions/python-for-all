"""Chapter 13: Inheritance, Composition and Data Classes

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch13_inheritance.py

or open the notebook and run the cells in order.
"""

# %% 13.1 Inheritance
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount

# %% 13.1 Inheritance
class SavingsAccount(Account):
    def __init__(self, owner, balance=0, rate=0.03):
        super().__init__(owner, balance)
        self.rate = rate

    def add_interest(self):
        self.deposit(round(self.balance * self.rate, 2))

s = SavingsAccount("Asha", 1000)
s.deposit(200)
s.add_interest()
print(s.owner, s.balance)

# %% 13.1 Inheritance
class CheckingAccount(Account):
    def __init__(self, owner, balance=0, overdraft=100):
        super().__init__(owner, balance)
        self.overdraft = overdraft

    def withdraw(self, amount):
        if amount > self.balance + self.overdraft:
            raise ValueError("overdraft limit reached")
        self.balance -= amount

c = CheckingAccount("Ben", 50)
c.withdraw(120)
print(c.balance)

# %% 13.1 Inheritance
print(isinstance(c, CheckingAccount), isinstance(c, Account))
print(isinstance(c, SavingsAccount))
print(issubclass(SavingsAccount, Account))
print([cls.__name__ for cls in CheckingAccount.__mro__])

# %% 13.1 Inheritance
accounts = [SavingsAccount("Asha", 500), CheckingAccount("Ben", 20),
            Account("Chen", 30)]
for acc in accounts:
    kind = type(acc).__name__
    try:
        acc.withdraw(60)
        print(f"{acc.owner:<5} {kind:<16}{acc.balance:>5}")
    except ValueError as err:
        print(f"{acc.owner:<5} {kind:<16}refused: {err}")

# %% 13.2 Your own exceptions
class InsufficientFunds(ValueError):
    """Raised when a withdrawal is larger than the money available."""

    def __init__(self, needed, available):
        super().__init__(f"need {needed}, only {available} available")
        self.shortfall = needed - available

class Account2(Account):
    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds(amount, self.balance)
        self.balance -= amount

# %% 13.2 Your own exceptions
acc = Account2("Dina", 80)
try:
    acc.withdraw(100)
except InsufficientFunds as err:
    print("Refused:", err)
    print("Short by", err.shortfall)
try:
    acc.withdraw(500)
except ValueError as err:
    print("Still a ValueError:", type(err).__name__)

# %% 13.3 Special methods: making objects work with operators
class Money:
    def __init__(self, cents):
        self.cents = cents

    def __repr__(self):
        return f"Money(${self.cents / 100:.2f})"

    def __add__(self, other):
        return Money(self.cents + other.cents)

    def __eq__(self, other):
        return self.cents == other.cents

    def __lt__(self, other):
        return self.cents < other.cents

# %% 13.3 Special methods: making objects work with operators
lunch, coffee = Money(1250), Money(375)
print(lunch + coffee)
print(Money(500) == Money(500), coffee < lunch)
print(sorted([lunch, coffee, Money(800)]))
print(max(lunch, coffee))

# %% 13.4 Data classes
from dataclasses import dataclass

@dataclass
class Book:
    title: str
    author: str
    pages: int = 0

b = Book("Dune", "Frank Herbert", 688)
print(b)
print(b.title, b == Book("Dune", "Frank Herbert", 688))
print(Book("Emma", "Jane Austen"))

# %% 13.4 Data classes
@dataclass(order=True, frozen=True)
class Version:
    major: int
    minor: int
    patch: int = 0

versions = [Version(3, 14), Version(3, 9, 7), Version(3, 13, 2)]
print(max(versions))
print(sorted(versions)[0])

# %% 13.6 Matching objects with match
@dataclass
class Circle:
    radius: float

@dataclass
class Rect:
    width: float
    height: float

# %% 13.6 Matching objects with match
def area(shape):
    match shape:
        case Circle(radius=r):
            return 3.14159 * r ** 2
        case Rect(width=w, height=h) if w == h:
            return w * w            # a square
        case Rect(width=w, height=h):
            return w * h
    raise TypeError(f"unknown shape {shape!r}")

# %% 13.6 Matching objects with match
for s in [Circle(1), Rect(3, 3), Rect(2, 5)]:
    print(f"{s!r:<26}{area(s):>8.2f}")

# %% 13.7 Putting it together: a playlist
from dataclasses import dataclass, field

@dataclass(frozen=True, order=True)
class Song:
    artist: str
    title: str
    seconds: int

    def __str__(self):
        m, s = divmod(self.seconds, 60)
        return f"{self.artist} - {self.title} ({m}:{s:02d})"

# %% 13.7 Putting it together: a playlist
@dataclass
class Playlist:
    name: str
    songs: list[Song] = field(default_factory=list)

    def add(self, song):
        if song in self.songs:
            raise ValueError(f"already in {self.name}: {song.title}")
        self.songs.append(song)

    def __len__(self):
        return len(self.songs)

    @property
    def duration(self):
        return sum(s.seconds for s in self.songs)

# %% 13.7 Putting it together: a playlist
mix = Playlist("Road trip")
for song in [Song("Queen", "Bohemian Rhapsody", 355),
             Song("ABBA", "Dancing Queen", 231),
             Song("Queen", "Don't Stop Me Now", 209)]:
    mix.add(song)
try:
    mix.add(Song("ABBA", "Dancing Queen", 231))
except ValueError as err:
    print("Error:", err)
print(f"{mix.name}: {len(mix)} songs, {mix.duration // 60} min")
for song in sorted(mix.songs):
    print(" ", song)
