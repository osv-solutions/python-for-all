"""Code from "18.6 Linting and formatting with ruff" that is shown in the book but not run on its own:
it needs your own data, a server or extra setup, or it is one step of an example
that the book builds up gradually. See the book for details."""

import os, sys
from statistics import mean
from grades import letter_grade,best_student

def print_summary(scores):
    for name,marks in scores.items():
        average=mean(marks)
        print(f"{name:<8}{average:5.1f}  {letter_grade(average)}")
    print(f"Students:", len(score))
    print("Top student:", best_student(scores))
