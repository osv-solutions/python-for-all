import pytest

from conversions import convert, format_result, parse_number, units


def test_length():
    assert convert(1, "Length", "miles", "kilometers") == 1.609344
    assert convert(12, "Length", "inches", "feet") == pytest.approx(1)


def test_weight():
    assert convert(1, "Weight", "kilograms", "pounds") == pytest.approx(
        2.20462262)


@pytest.mark.parametrize("value, source, target, expected", [
    (100, "degrees Celsius", "degrees Fahrenheit", 212),
    (-40, "degrees Fahrenheit", "degrees Celsius", -40),
    (0, "kelvins", "degrees Celsius", -273.15),
])
def test_temperature(value, source, target, expected):
    assert convert(value, "Temperature", source,
                   target) == pytest.approx(expected)


def test_below_absolute_zero():
    with pytest.raises(ValueError, match="absolute zero"):
        convert(-300, "Temperature", "degrees Celsius", "kelvins")


def test_units_must_match_the_category():
    with pytest.raises(ValueError, match="Choose two units"):
        convert(1, "Length", "meters", "pounds")


def test_parse_number():
    assert parse_number(" 1,200.5 ") == 1200.5
    with pytest.raises(ValueError, match="'ten' is not a number"):
        parse_number("ten")
    with pytest.raises(ValueError, match="Type a number"):
        parse_number("")


def test_format_result():
    assert format_result(3.28083989) == "3.2808"
    assert format_result(1609.344) == "1,609.344"
    assert format_result(212.0) == "212"
    assert format_result(-0.00001) == "0"


def test_units():
    assert units("Weight")[:2] == ["grams", "kilograms"]
    assert len(units("Temperature")) == 3
