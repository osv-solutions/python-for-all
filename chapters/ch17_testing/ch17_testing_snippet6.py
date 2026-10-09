"""Code from "17.9 Fixtures: shared setup" that is shown in the book but not run on its own:
it needs your own data, a server or extra setup, or it is one step of an example
that the book builds up gradually. See the book for details."""

import json


class Cart:
    ...                    # __init__, add and total as in Chapter 12

    def remove(self, name):
        del self._items[name]

    def save(self, path):
        path.write_text(json.dumps(self._items))

    def load(self, path):
        self._items = json.loads(path.read_text())
