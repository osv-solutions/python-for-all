"""Chapter 18: Type Hints and Clean Code

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch18_clean_code.py

or open the notebook and run the cells in order.
"""

# %% 18.3 Naming well
def chk(l, n):
    return [x for x in l if x[1] >= n]

def students_who_passed(results, pass_mark):
    return [row for row in results if row[1] >= pass_mark]

results = [("Ada", 92), ("Grace", 58), ("Alan", 75)]
print(chk(results, 60))
print(students_who_passed(results, 60))

# %% 18.3 Naming well
PRICE_PER_KG = 2.5
EXPRESS_FEE = 10

def shipping_cost(weight_kg, express=False):
    cost = weight_kg * PRICE_PER_KG
    if express:
        cost += EXPRESS_FEE
    return cost

print(shipping_cost(4), shipping_cost(4, express=True))

# %% 18.4 Type hints in depth
def add(a: int, b: int) -> int:
    return a + b

print(add(2, 3))
print(add("2", "3"))
print(add([1], [2]))
print(add.__annotations__)

# %% 18.4 Type hints in depth
def find_scores(scores: dict[str, list[int]],
                name: str) -> list[int] | None:
    """Return a student's scores, or None if they are unknown."""
    return scores.get(name)

scores = {"Ada": [92, 88], "Grace": [75, 81]}
print(find_scores(scores, "Ada"), find_scores(scores, "Alan"))

# %% 18.4 Type hints in depth
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    scores: list[int]
    mentor: Student | None = None

ada = Student("Ada", [92, 88])
alan = Student("Alan", [58, 49], mentor=ada)
print(alan.mentor)

# %% 18.4 Type hints in depth
from collections.abc import Callable

type Scores = dict[str, list[int]]
type Rule = Callable[[list[int]], float]

def apply_rule(scores: Scores, rule: Rule) -> dict[str, float]:
    return {name: rule(marks) for name, marks in scores.items()}

print(apply_rule({"Ada": [92, 88], "Grace": [75, 81]}, max))

# %% 18.7 Refactoring step by step
def calc(d):
    r = []
    for k in d:
        if d[k]:
            if len(d[k]) > 3:
                s = sorted(d[k])[1:]
            else:
                s = d[k]
            a = sum(s) / len(s)
            if a >= 60:
                if a >= 90:
                    r.append(k + ": " + str(round(a, 1)) + " honors")
                else:
                    r.append(k + ": " + str(round(a, 1)) + " pass")
            else:
                r.append(k + ": " + str(round(a, 1)) + " fail")
    return r

# %% 18.7 Refactoring step by step
cases = [
    {"Ada": [92, 88, 95, 40], "Grace": [75, 81], "Alan": []},
    {"Bo": [60], "Cy": [59.9], "Di": [90, 90, 90]},
    {},
]
expected = [calc(case) for case in cases]
print(expected[0])
print(expected[1])

# %% 18.7 Refactoring step by step
PASS_MARK = 60
HONORS_MARK = 90
MAX_KEPT_IN_FULL = 3

def counted_scores(scores: list[float]) -> list[float]:
    """Drop the lowest score if there are more than three."""
    if len(scores) > MAX_KEPT_IN_FULL:
        return sorted(scores)[1:]
    return scores

def result(average: float) -> str:
    """Return honors, pass or fail for an average score."""
    if average >= HONORS_MARK:
        return "honors"
    if average >= PASS_MARK:
        return "pass"
    return "fail"

# %% 18.7 Refactoring step by step
def report_lines(scores: dict[str, list[float]]) -> list[str]:
    """Return one line per student who has scores."""
    lines: list[str] = []
    for name, marks in scores.items():
        if not marks:
            continue
        counted = counted_scores(marks)
        average = sum(counted) / len(counted)
        lines.append(f"{name}: {round(average, 1)} {result(average)}")
    return lines


for line in report_lines(cases[1]):
    print(line)

# %% 18.7 Refactoring step by step
for case, old in zip(cases, expected):
    assert report_lines(case) == old
print("same results for", len(cases), "cases")
