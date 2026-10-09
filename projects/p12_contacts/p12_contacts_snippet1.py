"""Code from "Step 4: The contact book" that is shown in the book but not run on its own:
it needs your own data, a server or extra setup, or it is one step of an example
that the book builds up gradually. See the book for details."""

class ContactBook:
    ...

    def update(self, old_name: str, **changes: str) -> Contact:
        """Change some fields of a contact; return the new one."""
        old = self.get(old_name)
        new = replace(old, **changes)
        if name_key(new.name) != name_key(old.name):
            self._check_free(new.name)
        self.delete(old.name)
        self.add(new)
        return new
