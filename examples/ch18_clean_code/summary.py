"""Print each student's average and letter grade."""

from statistics import mean

from grades import best_student, letter_grade


def print_summary(scores: dict[str, list[int]]) -> None:
    """Print a line per student, the class size and the best."""
    for name, marks in scores.items():
        average = mean(marks)
        print(f"{name:<8}{average:5.1f}  {letter_grade(average)}")
    print("Students:", len(scores))
    print("Top student:", best_student(scores))


if __name__ == "__main__":
    scores = {"Ada": [92, 88], "Grace": [75, 81], "Alan": [58, 49]}
    print_summary(scores)
