"""Solutions to the Chapter 12 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch12_solutions.py

The explanations are in ch12_solutions.md."""

# %% Exercise 12.1
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __repr__(self):
        return f"Book({self.title!r}, {self.author!r}, {self.pages})"

books = [Book("Dune", "Frank Herbert", 688),
         Book("Emma", "Jane Austen", 474)]
print(books)

# %% Exercise 12.2
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __repr__(self):
        return f"Book({self.title!r}, {self.author!r}, {self.pages})"

    def is_long(self, limit=300):
        """Return True if the book has more pages than limit."""
        return self.pages > limit

# %% Exercise 12.2
shelf = [Book("Dune", "Frank Herbert", 688),
         Book("Emma", "Jane Austen", 474),
         Book("The Little Prince", "Antoine de Saint-Exupery", 96),
         Book("Animal Farm", "George Orwell", 112)]
for book in shelf:
    if book.is_long():
        print(book.title)
print("Over 500 pages:")
for book in shelf:
    if book.is_long(500):
        print(" ", book.title)

# %% Exercise 12.3
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.balance += amount
        self.history.append(("deposit", amount))

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        self.history.append(("withdrawal", amount))

# %% Exercise 12.3
def statement(self):
    """Return the history as lines, ending with the balance."""
    lines = []
    for kind, amount in self.history:
        sign = "+" if kind == "deposit" else "-"
        lines.append(f"{kind:<12}{sign}{amount:>9.2f}")
    lines.append(f"{'balance':<12}{self.balance:>10.2f}")
    return "\n".join(lines)

BankAccount.statement = statement

# %% Exercise 12.3
acc = BankAccount("Asha", 100)
acc.deposit(50)
acc.withdraw(30)
try:
    acc.withdraw(500)
except ValueError as err:
    print("Refused:", err)
acc.deposit(20)
print(acc.statement())
print(acc.history[0])

# %% Exercise 12.4
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def fahrenheit(self):
        return self.celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5 / 9

# %% Exercise 12.4
t = Temperature(25)
print(t.celsius, t.fahrenheit)
t.fahrenheit = 212
print(t.celsius, t.fahrenheit)
t.celsius = -40
print(t.fahrenheit)

# %% Exercise 12.5
class Counter:
    created = 0               # shared by every counter

    def __init__(self):
        self._value = 0
        Counter.created += 1

    def increment(self):
        self._value += 1

    def reset(self):
        self._value = 0

    @property
    def value(self):
        return self._value

# %% Exercise 12.5
clicks, visits = Counter(), Counter()
for _ in range(3):
    clicks.increment()
visits.increment()
print(clicks.value, visits.value, Counter.created)
clicks.reset()
print(clicks.value, visits.value)
try:
    clicks.value = 99
except AttributeError as err:
    print("Refused:", err)

# %% Exercise 12.6
def transfer(self, other, amount):
    """Move amount from this account to other, or change nothing."""
    if amount <= 0:
        raise ValueError("transfer must be positive")
    self.withdraw(amount)
    other.deposit(amount)

BankAccount.transfer = transfer

# %% Exercise 12.6
asha, ben = BankAccount("Asha", 100), BankAccount("Ben", 20)
asha.transfer(ben, 70)
print(asha.balance, ben.balance)
for amount in [500, -50]:
    try:
        asha.transfer(ben, amount)
    except ValueError as err:
        print(f"Transfer of {amount} refused: {err}")
print(asha.balance, ben.balance)
print(ben.history)

# %% Exercise 12.7
# Setup: recreates the context these solutions build on (from the chapter).
class Cart:
    """A shopping cart: item names with a price and a quantity."""
    def __init__(self, tax_rate=0.06):
        self.tax_rate = tax_rate
        self._items = {}             # name -> [price, quantity]

    def add(self, name, price, quantity=1):
        if price < 0 or quantity < 1:
            raise ValueError("bad price or quantity")
        item = self._items.setdefault(name, [price, 0])
        item[1] += quantity

    @property
    def total(self):
        subtotal = sum(p * q for p, q in self._items.values())
        return round(subtotal * (1 + self.tax_rate), 2)

# %% Exercise 12.7
def remove(self, name):
    """Remove an item and all of its quantity from the cart."""
    if name not in self._items:
        raise KeyError(name)
    del self._items[name]

def count(self):
    """Return the number of items, counting quantities."""
    return sum(quantity for price, quantity in self._items.values())

Cart.remove, Cart.count = remove, count

# %% Exercise 12.7
def receipt(self):
    """Return a receipt: one line per item, then tax and total."""
    lines = []
    for name, (price, qty) in self._items.items():
        cost = price * qty
        lines.append(
            f"{qty:>3} x {name:<16}{price:>7.2f}{cost:>9.2f}")
    subtotal = sum(p * q for p, q in self._items.values())
    lines.append("-" * 39)
    tax = self.total - subtotal
    lines.append(f"{'Tax':<29}{tax:>10.2f}")
    lines.append(f"{'Total':<29}{self.total:>10.2f}")
    return "\n".join(lines)

Cart.receipt = receipt

# %% Exercise 12.7
cart = Cart()
cart.add("Notebook", 3.50, 2)
cart.add("Backpack", 34.00)
cart.add("Pen", 1.25, 4)
cart.add("Notebook", 3.50)
cart.add("Water bottle", 12.99)
cart.remove("Pen")
try:
    cart.remove("Laptop")
except KeyError as err:
    print("Not in the cart:", err)
print(cart.count(), "items")
print(cart.receipt())
