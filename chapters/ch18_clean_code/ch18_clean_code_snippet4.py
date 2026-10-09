"""Code from "18.8 Docstrings and comments" that is shown in the book but not run on its own:
it needs your own data, a server or extra setup, or it is one step of an example
that the book builds up gradually. See the book for details."""

total = total * 1.08  # multiply total by 1.08

TAX_RATE = 0.08  # state sales tax, set by law each January
total = total * (1 + TAX_RATE)
