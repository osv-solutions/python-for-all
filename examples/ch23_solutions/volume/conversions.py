"""Unit conversions for the converter app: no tkinter here."""

# How many meters, kilograms or liters one of each unit is
FACTORS = {
    "Length": {"millimeters": 0.001, "centimeters": 0.01, "meters": 1,
               "kilometers": 1000, "inches": 0.0254, "feet": 0.3048,
               "yards": 0.9144, "miles": 1609.344},
    "Weight": {"grams": 0.001, "kilograms": 1,
               "ounces": 0.028349523125, "pounds": 0.45359237,
               "stones": 6.35029318},
    "Volume": {"milliliters": 0.001, "liters": 1,
               "US cups": 0.2365882365, "US gallons": 3.785411784},
}
TEMPERATURES = ["degrees Celsius", "degrees Fahrenheit", "kelvins"]
CATEGORIES = ["Length", "Weight", "Volume", "Temperature"]


def units(category):
    """Return the unit names of a category, in display order."""
    if category == "Temperature":
        return list(TEMPERATURES)
    return list(FACTORS[category])


def to_celsius(value, unit):
    if unit == "degrees Fahrenheit":
        return (value - 32) * 5 / 9
    if unit == "kelvins":
        return value - 273.15
    return value


def from_celsius(value, unit):
    if unit == "degrees Fahrenheit":
        return value * 9 / 5 + 32
    if unit == "kelvins":
        return value + 273.15
    return value


def convert(value, category, source, target):
    """Convert value from the source unit to the target unit."""
    if source not in units(category) or target not in units(category):
        raise ValueError(f"Choose two units of {category.lower()}")
    if category == "Temperature":
        celsius = to_celsius(value, source)
        if celsius < -273.15:
            raise ValueError("That is colder than absolute zero")
        return from_celsius(celsius, target)
    factors = FACTORS[category]
    return value * factors[source] / factors[target]


def parse_number(text):
    """Read a number such as '12.5' or '1,200'."""
    text = text.replace(",", "").strip()
    if not text:
        raise ValueError("Type a number to convert")
    try:
        return float(text)
    except ValueError:
        raise ValueError(f"{text!r} is not a number")


def format_result(number):
    """Show up to four decimals, without trailing zeros."""
    text = f"{number:,.4f}".rstrip("0").rstrip(".")
    return "0" if text == "-0" else text
