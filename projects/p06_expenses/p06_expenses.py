"""Project 6 (Intermediate): Expense Tracker with CSV Reports

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python p06_expenses.py

or open the notebook and run the cells in order.
"""

# %% Step 1: The data file
import csv
from datetime import date

FILENAME = "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]
CATEGORIES = ["food", "transport", "housing", "fun", "other"]

# %% Step 1: The data file
sample = """date,category,description,amount
2026-09-01,housing,September rent,1200.00
2026-09-03,food,Groceries,86.40
2026-09-09,transport,Bus pass,55.00
2026-09-14,fun,Concert tickets,90.00
2026-09-20,food,Groceries,74.25
2026-09-25,food,Dinner out,48.10
2026-10-01,housing,October rent,1200.00
2026-10-02,food,Groceries,92.30
2026-10-05,transport,Taxi,twenty
2026-10-06,fun,Cinema,24.00
"""
with open(FILENAME, "w", encoding="utf-8") as f:
    f.write(sample)

# %% Step 2: Load and validate
def parse_row(row):
    """Return a checked copy of the row, or raise ValueError."""
    when = date.fromisoformat(row["date"])
    if row["category"] not in CATEGORIES:
        raise ValueError(f"unknown category {row['category']!r}")
    amount = float(row["amount"])
    if amount <= 0:
        raise ValueError("amount must be positive")
    return {"date": when, "category": row["category"],
            "description": row["description"], "amount": amount}

# %% Step 2: Load and validate
def load_expenses():
    expenses = []
    try:
        with open(FILENAME, newline="", encoding="utf-8") as f:
            for line_no, row in enumerate(csv.DictReader(f), start=2):
                try:
                    expenses.append(parse_row(row))
                except ValueError as err:
                    print(f"Line {line_no} skipped: {err}")
    except FileNotFoundError:
        pass
    return expenses

expenses = load_expenses()
print(len(expenses), "expenses loaded")

# %% Step 3: Add an expense
def add_expense(when, category, description, amount):
    """Validate an expense given as text and append it to the file."""
    row = {"date": when.strip(), "category": category.strip().lower(),
           "description": description.strip(),
           "amount": amount.strip().lstrip("$")}
    expense = parse_row(row)
    row["amount"] = f"{expense['amount']:.2f}"
    with open(FILENAME, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writerow(row)
    return expense

# %% Step 3: Add an expense
for entry in [("2026-10-07", "Food", "Lunch", "$12.50"),
              ("2026-10-08", "clothes", "Jacket", "60")]:
    try:
        added = add_expense(*entry)
        expenses.append(added)
        print("Added:", added["description"], added["amount"])
    except ValueError as err:
        print("Not added:", err)

# %% Step 4: Spending by month and category
def totals(expenses):
    """Return {(month, category): total}, with months as "YYYY-MM"."""
    result = {}
    for e in expenses:
        key = (e["date"].strftime("%Y-%m"), e["category"])
        result[key] = result.get(key, 0) + e["amount"]
    return result

table = totals(expenses)
months = sorted({month for month, cat in table})
print(months)
print(f"{table[('2026-09', 'food')]:.2f}")

# %% Step 4: Spending by month and category
def report(expenses):
    table = totals(expenses)
    months = sorted({month for month, cat in table})
    print(f"{'':<10}" + "".join(f"{m:>10}" for m in months))
    for cat in CATEGORIES:
        cells = [table.get((m, cat), 0) for m in months]
        print(f"{cat:<10}" + "".join(f"{c:>10.2f}" for c in cells))
    print(f"{'total':<10}", end="")
    for m in months:
        month_total = sum(table.get((m, c), 0) for c in CATEGORIES)
        print(f"{month_total:>10.2f}", end="")
    print()

report(expenses)

# %% Step 5: Compare with a budget
BUDGET = {"food": 250, "transport": 80, "housing": 1200,
          "fun": 80, "other": 50}

def budget_check(expenses, month):
    table = totals(expenses)
    print(f"Budget check for {month}")
    for cat in CATEGORIES:
        spent = table.get((month, cat), 0)
        share = spent / BUDGET[cat]
        bar = "#" * min(round(share * 20), 30)
        flag = "  OVER" if spent > BUDGET[cat] else ""
        limit = f"{spent:>8.2f} / {BUDGET[cat]:<5}"
        print(f"  {cat:<10}{limit}{bar}{flag}")

budget_check(expenses, "2026-09")

# %% Step 6: Export a summary for a spreadsheet
def export_summary(expenses, filename="summary.csv"):
    table = totals(expenses)
    months = sorted({month for month, cat in table})
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["category"] + months)
        for cat in CATEGORIES:
            cells = [table.get((m, cat), 0) for m in months]
            writer.writerow([cat] + [f"{c:.2f}" for c in cells])
    return filename

name = export_summary(expenses)
print(open(name, encoding="utf-8").read(), end="")
