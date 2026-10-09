"""Chapter 9: Modules and the Standard Library

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch09_modules.py

or open the notebook and run the cells in order.
"""

# %% 9.1 Using a module
import math

print(math.sqrt(81), math.pi)
print(math.ceil(4.2), math.floor(4.8))
print(math.isclose(0.1 + 0.2, 0.3))

# %% 9.1 Using a module
from math import sqrt, pi
print(sqrt(2) * pi)

import statistics as st
print(st.mean([2, 4, 9]), st.median([2, 4, 9]))

# %% 9.3 Numbers: math and statistics
import statistics

times = [12.1, 11.4, 13.0, 11.4, 12.6, 30.2]
print(statistics.mean(times))
print(statistics.median(times))
print(statistics.mode(times))
print(round(statistics.stdev(times), 2))

# %% 9.4 Randomness: random and secrets
import random

random.seed(4)
deck = ["A", "K", "Q", "J", "10", "9"]
random.shuffle(deck)
print(deck)
print(random.sample(range(1, 50), 6))
print(round(random.uniform(1.5, 2.5), 3))

# %% 9.5 Dates and times: datetime
from datetime import date, timedelta

launch = date(2026, 10, 8)
print(launch, launch.year, launch.month, launch.day)
print(launch.strftime("%A, %d %B %Y"))
print(launch.weekday())

# %% 9.5 Dates and times: datetime
due = launch + timedelta(days=30)
print("Due:", due)
deadline = date(2026, 12, 25)
gap = deadline - launch
print(gap.days, "days to go")
print(date(2028, 3, 1) - date(2028, 2, 1))

# %% 9.6 Files and folders: pathlib
from pathlib import Path

report = Path("reports") / "2026" / "summary.txt"
print(report)
print(report.name, report.stem, report.suffix)
print(report.parent)

# %% 9.6 Files and folders: pathlib
folder = Path("notes")
folder.mkdir(exist_ok=True)
(folder / "monday.txt").write_text("Buy milk\n")
(folder / "tuesday.txt").write_text("Call Ravi\n")
print(sorted(p.name for p in folder.glob("*.txt")))
print((folder / "monday.txt").read_text().strip())
print((folder / "friday.txt").exists())

# %% 9.7 Writing your own modules
# Setup: recreates the context this solution builds on (not printed in the book).
from pathlib import Path
Path("temperature.py").write_text('''"""Convert temperatures between Celsius and Fahrenheit."""

FREEZING_F = 32


def c_to_f(celsius):
    """Return the temperature in degrees Fahrenheit."""
    return celsius * 9 / 5 + FREEZING_F


def f_to_c(fahrenheit):
    """Return the temperature in degrees Celsius."""
    return (fahrenheit - FREEZING_F) * 5 / 9
''')

# %% 9.7 Writing your own modules
import temperature

print(temperature.c_to_f(100))
print(round(temperature.f_to_c(98.6), 1))
print(temperature.FREEZING_F)

# %% 9.9 Putting it together: a trip planner
from datetime import date, timedelta
import statistics

def trip_dates(start, nights):
    """Return the list of dates from arrival to departure."""
    return [start + timedelta(days=n) for n in range(nights + 1)]

days = trip_dates(date(2026, 12, 20), 6)
print(f"Arrive {days[0]:%a %d %b}, leave {days[-1]:%a %d %b}")
weekend = [d for d in days if d.weekday() >= 5]
print("Weekend days:", ", ".join(f"{d:%a %d}" for d in weekend))

# %% 9.9 Putting it together: a trip planner
import math

costs = [180.0, 95.5, 120.0, 88.0, 240.0, 105.0, 60.0]
print(f"Total ${sum(costs):,.2f}, "
      f"typical day ${statistics.median(costs):.2f}")
print("Save $50 a week for", math.ceil(sum(costs) / 50), "weeks")
