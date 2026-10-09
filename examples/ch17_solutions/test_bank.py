import pytest

from bank import BankAccount


@pytest.fixture
def account():
    return BankAccount("Asha", 100)


def test_deposit(account):
    account.deposit(50)
    assert account.balance == 150


def test_withdraw(account):
    account.withdraw(30)
    assert account.balance == 70


def test_overdraw_is_refused(account):
    with pytest.raises(ValueError, match="insufficient"):
        account.withdraw(500)
    assert account.balance == 100


@pytest.mark.parametrize("amount", [0, -1, -50.5])
def test_bad_deposit_is_refused(account, amount):
    with pytest.raises(ValueError):
        account.deposit(amount)
    assert account.balance == 100
