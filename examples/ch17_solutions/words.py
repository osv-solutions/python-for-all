def word_count(path):
    """Return the number of words in a text file."""
    return len(path.read_text(encoding="utf-8").split())
