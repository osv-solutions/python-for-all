"""Project 14 (Advanced): Contact Book: a Tested, Packaged Command-Line App

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python p14_contacts.py

or open the notebook and run the cells in order.
"""

# %% Step 3: A contact that checks itself
# Setup: recreates the context this solution builds on (not printed in the book).
# Lets this script import the package from the examples folder
# without installing it (in the book: pip install -e .).
import sys
from pathlib import Path

for root in ("../../repo_static/examples", "../../examples"):
    src = Path(root, "p14_contactbook", "src")
    if src.exists():
        sys.path.insert(0, str(src.resolve()))

# %% Step 3: A contact that checks itself
from contactbook.models import Contact, InvalidContactError

print(Contact("  Ada   Lovelace ", " ADA@Example.com", "555-0101"))
for bad in [("Ada", "ada.example.com"), ("Ada", "", "call me")]:
    try:
        Contact(*bad)
    except InvalidContactError as err:
        print("refused:", err)

# %% Step 4: The contact book
from contactbook.book import ContactBook

book = ContactBook([Contact("Grace Hopper", "grace@example.com"),
                    Contact("Alan Turing", "alan@example.com")])
print([contact.name for contact in book.find("AN")])
print(book.update("alan turing", phone="555-0103"))
try:
    book.update("Alan Turing", name="grace HOPPER")
except Exception as err:
    print(type(err).__name__, "-", err)
