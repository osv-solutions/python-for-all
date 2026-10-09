"""Project 6 (Intermediate): Text Adventure

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python p06_adventure.py

The script asks you to type answers. To replay the answers used
in the book instead:

    python p06_adventure.py < p06_adventure.inputs.txt

You can also open the notebook and run the cells in order.
"""

# %% Step 1: Items and rooms
from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    name: str
    description: str
    portable: bool = True

# %% Step 1: Items and rooms
class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}              # direction -> Room
        self.items = []

    def blocked(self, player):
        """Return a reason the player can't enter, or None."""
        return None

    def describe(self):
        lines = [f"== {self.name} ==", self.description]
        lines += [f"You see: {item.name}" for item in self.items]
        lines.append("Exits: " + ", ".join(sorted(self.exits)))
        return "\n".join(lines)

# %% Step 2: A locked door
class LockedRoom(Room):
    def __init__(self, name, description, key_name):
        super().__init__(name, description)
        self.key_name = key_name
        self.locked = True

    def blocked(self, player):
        if self.locked and player.has(self.key_name):
            self.locked = False
            print(f"You unlock the door with the {self.key_name}.")
        if self.locked:
            return "The door is locked."
        return None

# %% Step 3: Building the world
OPPOSITE = {"north": "south", "south": "north", "east": "west",
            "west": "east", "up": "down", "down": "up"}


def connect(room, direction, other):
    room.exits[direction] = other
    other.exits[OPPOSITE[direction]] = room

# %% Step 3: Building the world
def build_world():
    hall = Room("Hall", "A dusty entrance hall. Portraits watch you.")
    kitchen = Room("Kitchen", "Copper pans hang over a cold stove.")
    library = Room("Library", "Shelves of books reach the ceiling.")
    vault = LockedRoom("Vault", "Gold glints in the dark.", "key")
    connect(hall, "north", library)
    connect(hall, "east", kitchen)
    connect(library, "east", vault)
    kitchen.items.append(Item("key", "A small brass key."))
    kitchen.items.append(
        Item("table", "A heavy oak table.", portable=False))
    library.items.append(
        Item("note", "It says: 'Bring the crown to the hall.'"))
    vault.items.append(Item("crown", "A crown set with rubies."))
    return hall

# %% Step 3: Building the world
hall = build_world()
print(hall.describe())
print()
print(hall.exits["east"].describe())

# %% Step 4: The player
class Player:
    def __init__(self, start):
        self.room = start
        self.inventory = []

    def has(self, name):
        return any(item.name == name for item in self.inventory)

    def go(self, direction):
        target = self.room.exits.get(direction)
        if target is None:
            return "You can't go that way."
        reason = target.blocked(self)
        if reason:
            return reason
        self.room = target
        return target.describe()

# %% Step 4: The player
def find(items, name):
    for item in items:
        if item.name == name:
            return item
    return None


def take(player, name):
    item = find(player.room.items, name)
    if item is None:
        return f"There is no {name} here."
    if not item.portable:
        return f"The {name} is too heavy to carry."
    player.room.items.remove(item)
    player.inventory.append(item)
    return f"You take the {name}."

# %% Step 4: The player
def drop(player, name):
    item = find(player.inventory, name)
    if item is None:
        return f"You don't have a {name}."
    player.inventory.remove(item)
    player.room.items.append(item)
    return f"You drop the {name}."


def examine(player, name):
    item = find(player.inventory + player.room.items, name)
    return item.description if item else f"You see no {name}."


def inventory(player):
    names = [item.name for item in player.inventory]
    return "You carry: " + (", ".join(names) or "nothing")

# %% Step 4: The player
player = Player(build_world())
print(player.go("west"))
print(player.go("north").splitlines()[0])
print(player.go("east"))
print(take(player, "note"), "|", inventory(player))

# %% Step 5: Understanding commands
def handle(player, line):
    match line.lower().split():
        case ["look"]:
            return player.room.describe()
        case ["go", direction]:
            return player.go(direction)
        case ["take", name]:
            return take(player, name)
        case ["drop", name]:
            return drop(player, name)
        case ["examine", name]:
            return examine(player, name)
        case ["inventory"] | ["i"]:
            return inventory(player)
        case _:
            return "I don't understand that."

# %% Step 5: Understanding commands
player = Player(build_world())
for line in ["Go East", "take table", "take key", "dance", "i"]:
    print(f"> {line}")
    print(handle(player, line))

# %% Step 6: The game loop
def play():
    start = build_world()
    player = Player(start)
    print(start.describe())
    while True:
        line = input("> ")
        if line.strip().lower() == "quit":
            print("Goodbye!")
            break
        print(handle(player, line))
        if player.room is start and player.has("crown"):
            print("You carry the crown into the hall. You win!")
            break

# %% Step 6: The game loop
play()
