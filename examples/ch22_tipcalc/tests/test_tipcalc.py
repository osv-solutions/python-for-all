import pytest

from tipcalc import split_bill
from tipcalc.cli import main


def test_split_bill():
    tip, total, share = split_bill(48.5, 20, 3)
    assert share == pytest.approx(19.4)


def test_main_prints_the_result(capsys):
    assert main(["48.50", "--percent", "20", "--people", "3"]) == 0
    out = capsys.readouterr().out
    assert out == "Tip $9.70, total $58.20, each pays $19.40\n"


def test_zero_people_is_an_error(capsys):
    assert main(["100", "--people", "0"]) == 1
    assert "at least 1" in capsys.readouterr().err


def test_bad_number_exits_with_2():
    with pytest.raises(SystemExit) as info:
        main(["100", "--percent", "lots"])
    assert info.value.code == 2
