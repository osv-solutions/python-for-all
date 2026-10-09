"""Chapter 12: Classes and Objects

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch12_classes.py

or open the notebook and run the cells in order.
"""

# %% 12.1 Objects everywhere
word = "python"
print(type(word), word.upper(), word.count("y"))
items = [3, 1, 2]
items.sort()
print(type(items), items)
print(isinstance(word, str), isinstance(items, str))

# %% 12.2 Defining a class
class BankAccount:
    """A bank account with an owner and a balance."""

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

acc = BankAccount("Asha", 100)
print(acc.owner, acc.balance)
print(type(acc).__name__, isinstance(acc, BankAccount))

# %% 12.2 Defining a class
a = BankAccount("Asha", 100)
b = BankAccount("Ben")
b.balance += 25
print(a.owner, a.balance, "|", b.owner, b.balance)

# %% 12.3 Methods
class BankAccount:
    """A bank account with an owner and a balance."""

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

# %% 12.3 Methods
acc = BankAccount("Asha", 100)
acc.deposit(50)
acc.withdraw(30)
print(acc.balance)
try:
    acc.withdraw(500)
except ValueError as err:
    print("Refused:", err)
print(acc.balance)

# %% 12.3 Methods
BankAccount.deposit(acc, 50)
print(acc.balance)

# %% 12.4 Printing objects
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

p = Point(3, 4)
print(p)
print([p, Point(0, 0)])
print(f"{p!r}")

# %% 12.5 Class attributes
class SavingsAccount:
    interest_rate = 0.03          # shared by every account
    accounts_opened = 0

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        SavingsAccount.accounts_opened += 1

    def add_interest(self):
        self.balance += self.balance * self.interest_rate

# %% 12.5 Class attributes
s1 = SavingsAccount("Asha", 1000)
s2 = SavingsAccount("Ben", 500)
s1.add_interest()
print(s1.balance, s2.balance, SavingsAccount.accounts_opened)
SavingsAccount.interest_rate = 0.05
s2.add_interest()
print(s2.balance)

# %% 12.6 Properties
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height

r = Rectangle(4, 3)
print(r.area)
r.width = 10
print(r.area)

# %% 12.6 Properties
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self):
        return self._balance

acc = BankAccount("Asha", 100)
print(acc.balance)

# %% 12.6 Properties
# This example stops with an error on purpose (see the book).
try:
    acc.balance = 1_000_000
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% 12.8 Putting it together: a shopping cart
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

# %% 12.8 Putting it together: a shopping cart
cart = Cart()
cart.add("Notebook", 3.50, 2)
cart.add("Backpack", 34.00)
cart.add("Notebook", 3.50)
print(cart.total)
try:
    cart.add("Pen", 1.25, 0)
except ValueError as err:
    print("Refused:", err)
print(len(cart._items), "different items")
