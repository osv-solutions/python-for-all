# Solutions: Chapter 12, Classes and Objects

Worked solutions to the exercises at the end of Chapter 12 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch12_solutions.ipynb`](ch12_solutions.ipynb) or the script `ch12_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 12.1

*Write a class `Book` with a title, an author and a number of pages, and a `__repr__` that shows all three. Create two books and print a list of them.*

```python
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
```

Output:

```text
[Book('Dune', 'Frank Herbert', 688), Book('Emma', 'Jane Austen', 474)]
```

A list shows its items with `__repr__`, so the output is `[Book('Dune', 'Frank Herbert', 688), Book('Emma', 'Jane Austen', 474)]`. The `!r` conversion puts quotes around the title and the author, which makes the text look like the code that would create the book again, the mark of a good `__repr__`. Without the method, the list would show two unhelpful entries of the form `<__main__.Book object at 0x...>`.

## Exercise 12.2

*Add a method `is_long(self, limit=300)` to `Book`, and use it to print the titles of the long books in a list.*

```python
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
```

The method returns the result of the comparison directly; there is no need for an `if` that returns `True` or `False`. Like any function parameter, `limit` has a default value, which a caller can override:

```python
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
```

Output:

```text
Dune
Emma
Over 500 pages:
  Dune
```

With the default limit of 300, *Dune* and *Emma* count as long. `book.is_long(500)` passes a different limit, and only *Dune*, with 688 pages, is left. Notice that the loop asks each book about itself: the rule for "long" lives in the class, so changing it later means changing one method, not every loop.

## Exercise 12.3

*Extend `BankAccount` with a `history` list that records every deposit and withdrawal as a tuple, and a method `statement()` that returns the history as readable lines.*

```python
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
```

The list is created in `__init__`, as the warning in the chapter recommends, so that every account gets its own history. Each method records the transaction only *after* its check has passed, so a refused withdrawal never appears in the history.

In your own file, `statement` simply goes inside the class, after `withdraw`. To keep each listing short here, it is written as a function and then stored in the class. This works because, as the chapter showed, a method is an ordinary function stored in the class, with the object as its first parameter:

```python
def statement(self):
    """Return the history as lines, ending with the balance."""
    lines = []
    for kind, amount in self.history:
        sign = "+" if kind == "deposit" else "-"
        lines.append(f"{kind:<12}{sign}{amount:>9.2f}")
    lines.append(f"{'balance':<12}{self.balance:>10.2f}")
    return "\n".join(lines)

BankAccount.statement = statement
```

Each tuple is unpacked into `kind` and `amount`, and a conditional expression (Chapter 4) picks the sign. The method *returns* the text instead of printing it, so the caller decides what to do with it: print it, save it to a file or send it by email. Now an account in use:

```python
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
```

Output:

```text
Refused: insufficient funds
deposit     +    50.00
withdrawal  -    30.00
deposit     +    20.00
balance         140.00
('deposit', 50)
```

The statement lists the three successful transactions and ends with the balance of 140.00: 100 plus 50, minus 30, plus 20. The refused withdrawal of 500 is missing, as it should be. The last line shows the raw data behind the statement, the tuple `('deposit', 50)`.

## Exercise 12.4

*Write a class `Temperature` that stores degrees Celsius and has a property `fahrenheit`, with a setter so that `t.fahrenheit = 212` updates the Celsius value.*

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def fahrenheit(self):
        return self.celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5 / 9
```

The object stores only one number, the Celsius value. The property computes Fahrenheit from it every time it is read, so the two can never disagree. `@fahrenheit.setter` marks a second method with the *same name* as the one that runs when the property is assigned to; it converts the new value back to Celsius and stores that.

```python
t = Temperature(25)
print(t.celsius, t.fahrenheit)
t.fahrenheit = 212
print(t.celsius, t.fahrenheit)
t.celsius = -40
print(t.fahrenheit)
```

Output:

```text
25 77.0
100.0 212.0
-40.0
```

25 °C is 77.0 °F. The assignment `t.fahrenheit = 212` looks like an ordinary attribute assignment, but it calls the setter, which sets `t.celsius` to 100.0, the boiling point of water. Changing `celsius` directly works too, and the property follows it: −40 is the one temperature that is the same on both scales.

## Exercise 12.5

*Write a class `Counter` with methods `increment()` and `reset()`, a property `value`, and a class attribute that counts how many counters have been created.*

```python
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
```

The count itself is stored in the internal attribute `_value`, and the property without a setter makes it read-only from outside, so the only ways to change a counter are its two methods. `created` belongs to the class, and `__init__` adds one to it for every new counter.

```python
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
```

Output:

```text
3 1 2
0 1
Refused: property 'value' of 'Counter' object has no setter
```

The two counters are independent: 3 clicks and 1 visit. `Counter.created` is 2, because two counters exist. Resetting `clicks` doesn't affect `visits`, and an attempt to set the value directly raises an `AttributeError`, because the property has no setter.

## Exercise 12.6

*Add a `transfer(self, other, amount)` method to `BankAccount` that withdraws from one account and deposits into another, leaving both unchanged if the withdrawal is refused.*

As in Exercise 12.3, the method is written as a function and then stored in the class from that exercise:

```python
def transfer(self, other, amount):
    """Move amount from this account to other, or change nothing."""
    if amount <= 0:
        raise ValueError("transfer must be positive")
    self.withdraw(amount)
    other.deposit(amount)

BankAccount.transfer = transfer
```

The order of the two steps matters. `withdraw` runs first, and if it raises a `ValueError`, the exception leaves `transfer` immediately, before `deposit` runs, so neither account has changed. The first check is needed too: `withdraw` only refuses amounts that are too *large*, so `withdraw(-50)` would pass its check and *add* 50 to the balance, and then `deposit(-50)` would fail, leaving the accounts out of step.

```python
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
```

Output:

```text
30 90
Transfer of 500 refused: insufficient funds
Transfer of -50 refused: transfer must be positive
30 90
[('deposit', 70)]
```

After the transfer of 70, Asha has 30 and Ben 90. The transfer of 500 is refused by `withdraw`, and the one of −50 by the new check; both balances are still 30 and 90 afterward. Because the method reuses `withdraw` and `deposit` instead of changing the balances itself, every rule of those methods applies to transfers too, and the transfer even appears in Ben's history as `('deposit', 70)`.

## Exercise 12.7

*Complete the `Cart` class with `remove(name)`, `count()` and `receipt()` methods, then fill a cart and print the receipt.*

<details>
<summary>Setup code: recreates the data and helpers from the chapter (click to show)</summary>

```python
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
```

</details>

The `Cart` class from the chapter is set up first, unchanged. The new methods are again written as functions and then stored in the class; in your own file, they go inside the class:

```python
def remove(self, name):
    """Remove an item and all of its quantity from the cart."""
    if name not in self._items:
        raise KeyError(name)
    del self._items[name]

def count(self):
    """Return the number of items, counting quantities."""
    return sum(quantity for price, quantity in self._items.values())

Cart.remove, Cart.count = remove, count
```

`remove` raises a `KeyError` with the item's name if it isn't in the cart, the same exception a dictionary raises for a missing key. `count` adds up the quantities, so three notebooks count as three items; it works like the `total` property, with a generator expression (Chapter 14). Now the receipt:

```python
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
```

Each item of the dictionary is a name and a `[price, quantity]` list, which the `for` line unpacks in one step with `name, (price, qty)`. The format specifications from Chapter 4 line the columns up. The tax is the difference between the total, which already includes it, and the subtotal. The program that uses the cart:

```python
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
```

Output:

```text
Not in the cart: 'Laptop'
5 items
  3 x Notebook           3.50    10.50
  1 x Backpack          34.00    34.00
  1 x Water bottle      12.99    12.99
---------------------------------------
Tax                                3.45
Total                             60.94
```

The pens are removed, and the attempt to remove a laptop prints `Not in the cart: 'Laptop'`. Five items are left: three notebooks, the backpack and the water bottle. The notebooks share one line of the receipt, because `add` raised the quantity of the existing entry. The items come to $57.49 before tax, the tax is $3.45 and the total $60.94. Code that uses the cart now calls `count()` instead of peeking at `_items`, as the chapter's example had to.
