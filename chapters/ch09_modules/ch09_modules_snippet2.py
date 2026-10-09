"""Code from "9.7 Writing your own modules" that is shown in the book but not run automatically:
it needs your own data, a server or extra setup. See the book for details."""

"""Convert temperatures between Celsius and Fahrenheit."""

FREEZING_F = 32


def c_to_f(celsius):
    """Return the temperature in degrees Fahrenheit."""
    return celsius * 9 / 5 + FREEZING_F


def f_to_c(fahrenheit):
    """Return the temperature in degrees Celsius."""
    return (fahrenheit - FREEZING_F) * 5 / 9
