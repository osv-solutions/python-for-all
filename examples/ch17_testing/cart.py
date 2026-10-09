"""The shopping cart from Chapter 12, with remove, save and load."""
import json


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

    def remove(self, name):
        del self._items[name]

    def save(self, path):
        path.write_text(json.dumps(self._items))

    def load(self, path):
        self._items = json.loads(path.read_text())
