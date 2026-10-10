"""Project 10 (Intermediate): Flashcard Study App with Spaced Repetition

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python p10_flashcards.py

The script asks you to type answers. To replay the answers used
in the book instead:

    python p10_flashcards.py < p10_flashcards.inputs.txt

You can also open the notebook and run the cells in order.
"""

# %% Step 1: How spaced repetition works
import json
import random
from dataclasses import dataclass, asdict
from datetime import date, timedelta

INTERVALS = [1, 2, 4, 8, 16]   # days to wait in boxes 1 to 5
TODAY = date(2026, 10, 12)     # use date.today() in a real program

# %% Step 2: A card
@dataclass
class Card:
    front: str
    back: str
    due: date
    box: int = 1

    def review(self, correct, today):
        """Move the card after an answer and set its next due date."""
        if correct:
            self.box = min(self.box + 1, len(INTERVALS))
        else:
            self.box = 1
        self.due = today + timedelta(days=INTERVALS[self.box - 1])

# %% Step 2: A card
card = Card("el gato", "the cat", TODAY)
day = TODAY
for correct in [True, True, False, True]:
    card.review(correct, day)
    print(f"{day:%a %d %b}: {'right' if correct else 'wrong'}, "
          f"box {card.box}, due {card.due:%a %d %b}")
    day = card.due

# %% Step 3: Checking answers
def normalize(text):
    text = " ".join(text.casefold().split())
    return text.removeprefix("the ")


def is_right(card, answer):
    options = card.back.split("/")
    return normalize(answer) in {normalize(o) for o in options}

# %% Step 3: Checking answers
car = Card("el coche", "the car / automobile", TODAY)
for answer in ["The car", "  automobile ", "CAR", "the bus"]:
    print(f"{answer!r:<16} {is_right(car, answer)}")

# %% Step 4: The deck
class Deck:
    def __init__(self, cards=None):
        self.cards = cards or []

    def add(self, front, back, today):
        front, back = front.strip(), back.strip()
        if not front or not back:
            raise ValueError("a card needs a front and a back")
        if any(c.front == front for c in self.cards):
            raise ValueError(f"there is already a card for {front!r}")
        self.cards.append(Card(front, back, today))

    def due(self, today):
        cards = [c for c in self.cards if c.due <= today]
        return sorted(cards, key=lambda c: (c.due, c.box))

# %% Step 4: The deck
WORDS = [("el perro", "the dog"), ("el gato", "the cat"),
         ("la casa", "the house"), ("el libro", "the book"),
         ("la mesa", "the table"), ("el agua", "the water"),
         ("la ventana", "the window"), ("el árbol", "the tree"),
         ("el coche", "the car / automobile"),
         ("la manzana", "the apple")]

deck = Deck()
for front, back in WORDS:
    deck.add(front, back, TODAY)
print(len(deck.due(TODAY)), "cards due today")
try:
    deck.add("el gato", "the cat", TODAY)
except ValueError as err:
    print("Refused:", err)

# %% Step 5: Saving and loading
def save_deck(deck, path):
    rows = [asdict(card) | {"due": card.due.isoformat()}
            for card in deck.cards]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)


def load_deck(path):
    try:
        with open(path, encoding="utf-8") as f:
            rows = json.load(f)
    except FileNotFoundError:
        return Deck()
    for row in rows:
        row["due"] = date.fromisoformat(row["due"])
    return Deck([Card(**row) for row in rows])

# %% Step 5: Saving and loading
save_deck(deck, "deck.json")
copy = load_deck("deck.json")
print(copy.cards == deck.cards, len(copy.cards))
with open("deck.json", encoding="utf-8") as f:
    print("".join(f.readlines()[:7]), end="")

# %% Step 6: A study session
def study(deck, today, limit=10):
    cards = deck.due(today)[:limit]
    if not cards:
        print("Nothing to review today. Well done!")
        return
    random.shuffle(cards)
    right = 0
    for card in cards:
        answer = input(f"{card.front} = ")
        correct = is_right(card, answer)
        card.review(correct, today)
        right += correct
        verdict = "Right!" if correct else f"No: {card.back}."
        print(f"  {verdict} Box {card.box}, due {card.due:%a %d %b}")
    print(f"{right} of {len(cards)} right")

# %% Step 6: A study session
random.seed(2)
study(deck, TODAY, limit=5)

# %% Step 7: Watching the schedule
def simulate(days, chance=0.8):
    deck = Deck()
    for front, back in WORDS:
        deck.add(front, back, TODAY)
    total = 0
    for n in range(days):
        day = TODAY + timedelta(days=n)
        cards = deck.due(day)
        for card in cards:
            card.review(random.random() < chance, day)
        total += len(cards)
        print(f"{day:%a %d %b} {len(cards):>3} {'#' * len(cards)}")
    return deck, total

# %% Step 7: Watching the schedule
random.seed(4)
sim_deck, total = simulate(28)
print(total, "reviews instead of", 28 * len(WORDS))

# %% Step 8: Statistics and the menu
from collections import Counter


def stats(deck, today):
    boxes = Counter(card.box for card in deck.cards)
    for box, wait in enumerate(INTERVALS, start=1):
        count = boxes[box]
        bar = "#" * count
        print(f"Box {box}, {wait:>2}-day wait: {count:>2} {bar}")
    due = len(deck.due(today))
    print(f"{due} of {len(deck.cards)} cards due today")


stats(sim_deck, TODAY + timedelta(days=28))

# %% Step 8: Statistics and the menu
def main(path="deck.json"):
    deck = load_deck(path)
    while True:
        match input("study, add, stats or quit? ").strip().lower():
            case "study":
                study(deck, TODAY)
            case "add":
                try:
                    deck.add(input("Front: "), input("Back: "), TODAY)
                except ValueError as err:
                    print("Not added:", err)
            case "stats":
                stats(deck, TODAY)
            case "quit":
                break
        save_deck(deck, path)

# %% Step 8: Statistics and the menu
main()
