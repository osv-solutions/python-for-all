"""Code from "17.6 Testing errors with pytest.raises" that is shown in the book but not run on its own:
it needs your own data, a server or extra setup, or it is one step of an example
that the book builds up gradually. See the book for details."""

import pytest


def test_negative_age_is_rejected():
    with pytest.raises(ValueError):
        ticket_price(-1)


def test_error_message_shows_the_age():
    with pytest.raises(ValueError, match="negative: -3"):
        ticket_price(-3)
