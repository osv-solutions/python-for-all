from wordcount import count_lines, count_words
from wordcount.cli import main


def test_count_words():
    assert count_words("the quick  brown\nfox") == 4
    assert count_words("") == 0


def test_count_lines():
    assert count_lines("one\ntwo\nthree\n") == 3


def test_main_counts_a_file(tmp_path, capsys):
    path = tmp_path / "poem.txt"
    path.write_text("Tyger Tyger, burning bright,\nIn the forests\n")
    assert main([str(path), "--lines"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("     2 lines     7 words")


def test_missing_file_gives_exit_code_1(tmp_path, capsys):
    assert main([str(tmp_path / "missing.txt")]) == 1
    assert "No such file" in capsys.readouterr().err
