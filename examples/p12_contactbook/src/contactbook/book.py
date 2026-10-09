"""The contact book: add, find, change and delete contacts."""

from collections.abc import Iterable
from dataclasses import replace

from contactbook.models import Contact, ContactError


class DuplicateContactError(ContactError):
    """A contact with this name is already in the book."""


class ContactNotFoundError(ContactError):
    """No contact has this name."""


def name_key(name: str) -> str:
    """The form of a name used to compare names."""
    return " ".join(name.split()).casefold()


class ContactBook:
    """Contacts, kept by name; names are unique, ignoring case."""

    def __init__(self, contacts: Iterable[Contact] = ()) -> None:
        self._contacts: dict[str, Contact] = {}
        for contact in contacts:
            self.add(contact)

    def _check_free(self, name: str) -> str:
        """Return the key for name, if no contact has that name."""
        key = name_key(name)
        if key in self._contacts:
            taken = self._contacts[key].name
            raise DuplicateContactError(
                f"{taken} is already in the book"
            )
        return key

    def add(self, contact: Contact) -> None:
        self._contacts[self._check_free(contact.name)] = contact

    def __len__(self) -> int:
        return len(self._contacts)

    def get(self, name: str) -> Contact:
        try:
            return self._contacts[name_key(name)]
        except KeyError:
            raise ContactNotFoundError(
                f"no contact named {name}"
            ) from None

    def all(self) -> list[Contact]:
        """Every contact, sorted by name."""
        return sorted(
            self._contacts.values(),
            key=lambda contact: contact.name.casefold(),
        )

    def find(self, text: str) -> list[Contact]:
        """Contacts whose name or email contains text, any case."""
        text = text.casefold()
        return [
            contact
            for contact in self.all()
            if text in contact.name.casefold()
            or text in contact.email
        ]

    def update(self, old_name: str, **changes: str) -> Contact:
        """Change some fields of a contact; return the new one."""
        old = self.get(old_name)
        new = replace(old, **changes)
        if name_key(new.name) != name_key(old.name):
            self._check_free(new.name)
        self.delete(old.name)
        self.add(new)
        return new

    def delete(self, name: str) -> Contact:
        contact = self.get(name)
        del self._contacts[name_key(contact.name)]
        return contact
