"""Code from "17.7 Comparing floats with pytest.approx" that is shown in the book but not run on its own:
it needs your own data, a server or extra setup, or it is one step of an example
that the book builds up gradually. See the book for details."""

def test_split_bill():
    tip, total, share = split_bill(48.5, 20, 3)
    assert tip == pytest.approx(9.7)
    assert total == pytest.approx(58.2)
    assert share == pytest.approx(19.4)
