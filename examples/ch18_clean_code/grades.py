"""Summarize the scores of a class: averages and letter grades."""

from statistics import mean

PASS_MARK = 60
GRADE_BOUNDS = [(90, "A"), (80, "B"), (70, "C"), (PASS_MARK, "D")]


def letter_grade(score: float) -> str:
    """Return the letter grade for a score from 0 to 100."""
    for bound, letter in GRADE_BOUNDS:
        if score >= bound:
            return letter
    return "F"


def best_student(scores: dict[str, list[int]]) -> str | None:
    """Return the student with the highest average, or None."""
    if not scores:
        return None
    return max(scores, key=lambda name: mean(scores[name]))


if __name__ == "__main__":
    scores = {"Ada": [92, 88], "Grace": [75, 81], "Alan": [58, 49]}
    top = best_student(scores)
    if top is not None:
        print(top.upper(), letter_grade(85))
