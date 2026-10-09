"""Project 8 (Intermediate): Tic-Tac-Toe with a Computer Opponent

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python p08_tictactoe.py

The script asks you to type answers. To replay the answers used
in the book instead:

    python p08_tictactoe.py < p08_tictactoe.inputs.txt

You can also open the notebook and run the cells in order.
"""

# %% Step 1: The board
from dataclasses import dataclass

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8),      # rows
         (0, 3, 6), (1, 4, 7), (2, 5, 8),      # columns
         (0, 4, 8), (2, 4, 6)]                 # diagonals

# %% Step 1: The board
@dataclass(frozen=True)
class Board:
    cells: tuple = (" ",) * 9

    def __str__(self):
        rows = [" | ".join(self.cells[r:r + 3]) for r in (0, 3, 6)]
        return "\n--+---+--\n".join(rows)

    def free(self):
        return [i for i, cell in enumerate(self.cells) if cell == " "]

    def place(self, i, mark):
        cells = list(self.cells)
        cells[i] = mark
        return Board(tuple(cells))

# %% Step 1: The board
print(Board(tuple("123456789")))
board = Board().place(4, "X").place(0, "O")
print(board.free())

# %% Step 2: Who has won?
def winner(board):
    """Return "X" or "O" if a player has three in a row, else None."""
    for line in LINES:
        marks = {board.cells[i] for i in line}
        if len(marks) == 1 and marks != {" "}:
            return marks.pop()
    return None


def game_over(board):
    return winner(board) is not None or not board.free()


def other(mark):
    return "O" if mark == "X" else "X"

# %% Step 2: Who has won?
board = Board(tuple("XXXOO    "))
print(board, winner(board), game_over(board), sep="\n")

# %% Step 3: Players are functions
import random


def random_player(board, mark):
    return random.choice(board.free())


def human_player(board, mark):
    print(board)
    while True:
        text = input(f"Your move, {mark} (1-9): ").strip()
        if text.isdigit() and int(text) - 1 in board.free():
            return int(text) - 1
        print("Please pick a free square from 1 to 9.")

# %% Step 3: Players are functions
def play(x_player, o_player):
    board, mark = Board(), "X"
    players = {"X": x_player, "O": o_player}
    while not game_over(board):
        square = players[mark](board, mark)
        board = board.place(square, mark)
        mark = other(mark)
    return board, winner(board) or "draw"

# %% Step 3: Players are functions
from collections import Counter


def tournament(x_player, o_player, games=100):
    return Counter(play(x_player, o_player)[1] for _ in range(games))


random.seed(1)
print(tournament(random_player, random_player))

# %% Step 4: A player with rules
def rule_player(board, mark):
    """Win, else block, else center, corners, sides."""
    for who in (mark, other(mark)):
        for i in board.free():
            if winner(board.place(i, who)) == who:
                return i
    for i in (4, 0, 2, 6, 8, 1, 3, 5, 7):
        if i in board.free():
            return i


print(tournament(random_player, rule_player))

# %% Step 5: A perfect player
from functools import lru_cache


@lru_cache(maxsize=None)
def score(board, mark):
    """The result for mark, about to move: 1 win, 0 draw, -1 loss."""
    if winner(board):
        return -1                # the opponent's last move won
    if not board.free():
        return 0                 # a full board without a winner
    return max(-score(board.place(i, mark), other(mark))
               for i in board.free())

# %% Step 5: A perfect player
def perfect_player(board, mark):
    def value(i):                # how good square i is for mark
        return -score(board.place(i, mark), other(mark))
    return max(board.free(), key=value)


print(perfect_player(Board(), "X"))
print(score.cache_info())

# %% Step 5: A perfect player
print(tournament(random_player, perfect_player))
print(tournament(rule_player, perfect_player))
print(tournament(perfect_player, perfect_player))

# %% Step 6: Play against it
board, result = play(human_player, perfect_player)
print(board)
print("Result:", result)
