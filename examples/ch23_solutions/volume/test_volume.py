import pytest

from conversions import CATEGORIES, convert, units


def test_volume():
    assert "Volume" in CATEGORIES
    assert units("Volume")[1] == "liters"
    assert convert(1, "Volume", "US gallons", "US cups") == (
        pytest.approx(16))
    assert convert(500, "Volume", "milliliters", "liters") == 0.5
