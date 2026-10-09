def is_valid_username(name):
    """3-15 letters, digits or _, not starting with a digit."""
    return (3 <= len(name) <= 15
            and all(c.isalnum() or c == "_" for c in name)
            and not name[0].isdigit())
