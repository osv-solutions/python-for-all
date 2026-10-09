"""Chapter 16: Virtual Environments and Packages

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch16_packages.py

or open the notebook and run the cells in order.
"""

# %% 16.4 Installing packages with pip
from tabulate import tabulate

rows = [["Mercury", 0.39, 88], ["Venus", 0.72, 225],
        ["Earth", 1.00, 365], ["Mars", 1.52, 687]]
headers = ["Planet", "Distance (AU)", "Year (days)"]
print(tabulate(rows, headers=headers))
