"""Exercise 18.3: a student's lowest score."""

type Scores = dict[str, list[int]]


def lowest_score(scores: Scores, name: str) -> int | None:
    """Return the student's lowest score, or None if unknown."""
    if name not in scores:
        return None
    return min(scores[name])


scores = {"Ada": [92, 88], "Grace": [75, 81]}
lowest = lowest_score(scores, "Ada")
if lowest is not None:
    print(lowest * 2)
