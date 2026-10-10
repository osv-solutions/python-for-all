import pytest

from contactbook.book import (
    ContactBook,
    ContactNotFoundError,
    DuplicateContactError,
)
from contactbook.models import Contact

EVERYONE = ["Ada Lovelace", "Alan Turing", "Grace Hopper"]


@pytest.fixture
def book():
    return ContactBook(
        [
            Contact("Grace Hopper", "grace@example.com", "555-0102"),
            Contact("Ada Lovelace", "ada@example.com", "555-0101"),
            Contact("Alan Turing", "alan.turing@example.com"),
        ]
    )


def test_all_is_sorted_by_name(book):
    names = [contact.name for contact in book.all()]
    assert names == EVERYONE


def test_duplicate_names_are_refused_in_any_case(book):
    with pytest.raises(DuplicateContactError):
        book.add(Contact("ada  LOVELACE"))
    assert len(book) == 3


@pytest.mark.parametrize(
    "text, expected",
    [
        ("ada", ["Ada Lovelace"]),
        ("TUR", ["Alan Turing"]),
        ("example.com", EVERYONE),
        ("babbage", []),
    ],
)
def test_find_matches_part_of_name_or_email(book, text, expected):
    assert [contact.name for contact in book.find(text)] == expected


def test_update_changes_only_the_given_fields(book):
    book.update("grace hopper", phone="555-0199")
    grace = book.get("Grace Hopper")
    assert (grace.email, grace.phone) == (
        "grace@example.com",
        "555-0199",
    )


def test_rename(book):
    book.update("Alan Turing", name="Alan M. Turing")
    assert (
        book.get("alan m. turing").email == "alan.turing@example.com"
    )
    with pytest.raises(ContactNotFoundError):
        book.get("Alan Turing")


def test_rename_to_an_existing_name_is_refused(book):
    with pytest.raises(DuplicateContactError):
        book.update("Alan Turing", name="Ada Lovelace")


def test_delete(book):
    assert book.delete("Ada Lovelace").email == "ada@example.com"
    assert len(book) == 2
    with pytest.raises(
        ContactNotFoundError, match="no contact named Ada"
    ):
        book.delete("Ada Lovelace")
