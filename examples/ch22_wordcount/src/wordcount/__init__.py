"""Count the words and lines in text."""


def count_words(text):
    """Return the number of words in text."""
    return len(text.split())


def count_lines(text):
    """Return the number of lines in text."""
    return len(text.splitlines())
