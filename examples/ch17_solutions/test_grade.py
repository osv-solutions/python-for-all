import pytest

from grade import grade


@pytest.mark.parametrize("score, letter", [
    (100, "A"), (90, "A"), (89, "B"), (80, "B"),
    (79, "C"), (70, "C"), (69, "F"), (0, "F"),
])
def test_grade(score, letter):
    assert grade(score) == letter
