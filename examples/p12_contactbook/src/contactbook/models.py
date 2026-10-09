"""A single contact, checked when it is created."""

from dataclasses import dataclass

PHONE_CHARACTERS = set("0123456789 +-().")
MIN_PHONE_DIGITS = 7


class ContactError(Exception):
    """Base class for every error the contact book reports."""


class InvalidContactError(ContactError):
    """A name, email address or phone number is not valid."""


def is_email(text: str) -> bool:
    """Check the shape of an address: name@domain.tld."""
    user, at, domain = text.partition("@")
    return bool(
        user
        and at
        and "." in domain.strip(".")
        and "@" not in domain
        and " " not in text
    )


def is_phone(text: str) -> bool:
    """Allow digits, spaces and + - ( ) . with 7+ digits."""
    digits = sum(char.isdigit() for char in text)
    return (
        set(text) <= PHONE_CHARACTERS and digits >= MIN_PHONE_DIGITS
    )


@dataclass
class Contact:
    name: str
    email: str = ""
    phone: str = ""

    def __post_init__(self) -> None:
        self.name = " ".join(self.name.split())
        self.email = self.email.strip().lower()
        self.phone = self.phone.strip()
        if not self.name:
            raise InvalidContactError("a contact needs a name")
        if self.email and not is_email(self.email):
            raise InvalidContactError(f"invalid email: {self.email}")
        if self.phone and not is_phone(self.phone):
            raise InvalidContactError(f"invalid phone: {self.phone}")
