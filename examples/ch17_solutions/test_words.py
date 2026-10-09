from words import word_count


def test_short_file(tmp_path):
    path = tmp_path / "poem.txt"
    path.write_text("The rain in Spain\nfalls mainly\n")
    assert word_count(path) == 6


def test_empty_file(tmp_path):
    path = tmp_path / "empty.txt"
    path.write_text("")
    assert word_count(path) == 0
