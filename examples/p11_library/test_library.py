from datetime import date

import pytest

from library import (Library, LibraryError, NotFoundError, RuleError,
                     most_borrowed, overdue, search)

DAY = date(2026, 10, 1)


@pytest.fixture
def lib():
    library = Library(":memory:")
    library.add_book("111", "Dune", "Frank Herbert", 1965, copies=2)
    library.add_book("222", "Emma", "Jane Austen", 1815)
    library.add_member("Ada", "ada@example.com", DAY)
    library.add_member("Ravi", "ravi@example.com", DAY)
    yield library
    library.close()


def test_borrow_sets_due_date(lib):
    loan = lib.borrow(1, 1, DAY)
    assert loan.due == date(2026, 10, 15)
    assert loan.returned is None


def test_last_copy_cannot_be_lent_twice(lib):
    lib.borrow(2, 1, DAY)
    with pytest.raises(RuleError, match="Emma"):
        lib.borrow(2, 2, DAY)


def test_member_may_hold_three_loans(lib):
    lib.add_book("333", "Persuasion", "Jane Austen", 1817)
    for book_id in (1, 2, 3):
        lib.borrow(book_id, 1, DAY)
    with pytest.raises(RuleError, match="Ada already has 3"):
        lib.borrow(1, 1, DAY)


@pytest.mark.parametrize("returned, fine", [
    (date(2026, 10, 14), 0), (date(2026, 10, 15), 0),
    (date(2026, 10, 16), 0.25), (date(2026, 10, 25), 2.5),
])
def test_fine_for_a_return(lib, returned, fine):
    loan = lib.borrow(1, 1, DAY)
    assert lib.give_back(loan.id, returned).fine(returned) == fine


def test_returning_twice_is_refused(lib):
    loan = lib.borrow(1, 1, DAY)
    lib.give_back(loan.id, DAY)
    with pytest.raises(RuleError):
        lib.give_back(loan.id, DAY)


@pytest.mark.parametrize("book_id, member_id", [(9, 1), (1, 9)])
def test_unknown_ids_are_refused(lib, book_id, member_id):
    with pytest.raises(NotFoundError):
        lib.borrow(book_id, member_id, DAY)


def test_duplicate_isbn_is_refused(lib):
    with pytest.raises(LibraryError, match="UNIQUE"):
        lib.add_book("111", "Dune Messiah", "Frank Herbert", 1969)


def test_search_ignores_case(lib):
    titles = [book.title for book in search(lib, "AUSTEN")]
    assert titles == ["Emma"]


def test_reports(lib):
    lib.borrow(1, 1, DAY)
    lib.borrow(1, 2, date(2026, 10, 5))
    late = overdue(lib, date(2026, 10, 17))
    assert [(r["name"], r["days"], r["fine"]) for r in late] == [
        ("Ada", 2, "$0.50")]
    assert [tuple(r) for r in most_borrowed(lib, 2)] == [
        ("Dune", 2), ("Emma", 0)]


def test_data_survives_closing(tmp_path):
    path = tmp_path / "library.db"
    first = Library(path)
    first.add_member("Ada", "ada@example.com", DAY)
    first.close()
    second = Library(path)
    assert second.member(1).name == "Ada"
    second.close()
