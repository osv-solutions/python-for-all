import tkinter as tk

import pytest

from app import ConverterApp


@pytest.fixture
def app():
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no display to create a window on")
    root.withdraw()
    yield ConverterApp(root)
    root.destroy()


def test_a_bad_value_shows_a_message(app):
    app.value.set("ten")
    assert app.result.get() == ""
    assert app.message.get() == "'ten' is not a number"


def test_starts_with_the_first_two_units(app):
    assert app.source.get() == "millimeters"
    assert app.target.get() == "centimeters"
    assert app.result.get() == "0.1 centimeters"


def test_typing_updates_the_result(app):
    app.source.set("meters")
    app.target.set("feet")
    app.value.set("10")
    assert app.result.get() == "32.8084 feet"
    assert app.message.get() == ""


def test_swap_and_category(app):
    app.category.set("Temperature")
    app.choose_category()
    app.value.set("100")
    assert app.result.get() == "212 degrees Fahrenheit"
    app.swap()
    assert app.result.get() == "37.7778 degrees Celsius"
