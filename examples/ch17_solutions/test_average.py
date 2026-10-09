import pytest

from average import average


def test_whole_numbers():
    assert average([2, 4, 6]) == 4


def test_single_number():
    assert average([5]) == 5


def test_floats():
    assert average([0.1, 0.2, 0.3]) == pytest.approx(0.2)


def test_empty_list_raises():
    with pytest.raises(ZeroDivisionError):
        average([])
