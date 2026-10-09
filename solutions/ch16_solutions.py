"""Solutions to the Chapter 16 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch16_solutions.py

The explanations are in ch16_solutions.md."""

# %% Exercise 16.3
from tabulate import tabulate

rows = [["Mercury", 0.39, 88], ["Venus", 0.72, 225],
        ["Earth", 1.00, 365], ["Mars", 1.52, 687]]
headers = ["Planet", "Distance (AU)", "Year (days)"]
for style in ["grid", "github", "simple_outline"]:
    print(style)
    print(tabulate(rows, headers=headers, tablefmt=style))
    print()

# %% Exercise 16.7
# Setup: recreates the context these solutions build on (from the chapter).
import csv
from datetime import date
from pathlib import Path

CATEGORIES = ["food", "transport", "housing", "fun", "other"]
Path("expenses.csv").write_text("""date,category,description,amount
2026-09-01,housing,September rent,1200.00
2026-09-03,food,Groceries,86.40
2026-09-09,transport,Bus pass,55.00
2026-09-14,fun,Concert tickets,90.00
2026-09-20,food,Groceries,74.25
2026-09-25,food,Dinner out,48.10
2026-10-01,housing,October rent,1200.00
2026-10-02,food,Groceries,92.30
2026-10-06,fun,Cinema,24.00
""", encoding="utf-8")

# %% Exercise 16.7
# Setup: recreates the context these solutions build on (from the chapter).
with open("expenses.csv", newline="", encoding="utf-8") as f:
    expenses = [{"date": date.fromisoformat(r["date"]),
                 "category": r["category"],
                 "amount": float(r["amount"])}
                for r in csv.DictReader(f)]

def totals(expenses):
    """Return {(month, category): total}, with months as "YYYY-MM"."""
    result = {}
    for e in expenses:
        key = (e["date"].strftime("%Y-%m"), e["category"])
        result[key] = result.get(key, 0) + e["amount"]
    return result

# %% Exercise 16.7
from tabulate import tabulate

def report(expenses):
    table = totals(expenses)
    months = sorted({month for month, cat in table})
    rows = [[cat] + [table.get((m, cat), 0) for m in months]
            for cat in CATEGORIES]
    month_totals = [sum(table.get((m, c), 0) for c in CATEGORIES)
                    for m in months]
    rows.append(["total"] + month_totals)
    print(tabulate(rows, headers=[""] + months, floatfmt=".2f"))

report(expenses)
