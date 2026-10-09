import pytest

from usernames import is_valid_username


@pytest.mark.parametrize("name", [
    "ada", "grace_hopper", "x_1", "a" * 15,
])
def test_valid(name):
    assert is_valid_username(name)


@pytest.mark.parametrize("name", [
    "ab", "a" * 16, "has space", "dash-name", "9lives", "",
])
def test_invalid(name):
    assert not is_valid_username(name)
