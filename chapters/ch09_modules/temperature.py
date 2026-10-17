"""Convert temperatures between Celsius and Fahrenheit."""

FREEZING_F = 32


def c_to_f(celsius):
    """Return the temperature in degrees Fahrenheit."""
    return celsius * 9 / 5 + FREEZING_F


def f_to_c(fahrenheit):
    """Return the temperature in degrees Celsius."""
    return (fahrenheit - FREEZING_F) * 5 / 9
