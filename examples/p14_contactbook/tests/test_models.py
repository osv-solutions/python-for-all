import pytest

from contactbook.models import Contact, InvalidContactError


def test_fields_are_tidied():
    contact = Contact(
        "  Ada   Lovelace ", " ADA@Example.com ", "555-0101 "
    )
    assert contact == Contact(
        "Ada Lovelace", "ada@example.com", "555-0101"
    )


def test_email_and_phone_are_optional():
    assert Contact("Grace Hopper").email == ""


@pytest.mark.parametrize(
    "name, email, phone",
    [
        ("   ", "", ""),
        ("Ada", "ada.example.com", ""),
        ("Ada", "ada@example", ""),
        ("Ada", "ada@@example.com", ""),
        ("Ada", "", "555-01"),
        ("Ada", "", "call me"),
    ],
)
def test_invalid_details_are_refused(name, email, phone):
    with pytest.raises(InvalidContactError):
        Contact(name, email, phone)
