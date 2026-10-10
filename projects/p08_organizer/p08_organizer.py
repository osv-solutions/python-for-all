"""Project 8 (Intermediate): File Organizer

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python p08_organizer.py

The script asks you to type answers. To replay the answers used
in the book instead:

    python p08_organizer.py < p08_organizer.inputs.txt

You can also open the notebook and run the cells in order.
"""

# %% Step 1: A folder to practice on
from pathlib import Path

downloads = Path("downloads")
downloads.mkdir(exist_ok=True)
samples = {"holiday.jpg": 2400, "scan.PDF": 800, "budget.xlsx": 120,
           "notes.txt": 3, "song.mp3": 4100, "photos.zip": 9800,
           "logo.png": 45, "report.pdf": 950, "setup.part": 300,
           "data.csv": 12, "README": 1, ".DS_Store": 6}
for name, kb in samples.items():
    (downloads / name).write_bytes(b"x" * kb * 1024)
print(len(list(downloads.iterdir())), "files")

# %% Step 2: Sorting rules
FOLDERS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Spreadsheets": [".xlsx", ".csv"],
    "Audio": [".mp3", ".wav"],
    "Archives": [".zip", ".tar", ".gz"],
}
FOLDER_FOR = {ext: folder for folder, exts in FOLDERS.items()
              for ext in exts}
SKIP = {".part", ".crdownload", ".tmp"}      # unfinished downloads

print(FOLDER_FOR[".png"], FOLDER_FOR[".csv"], len(FOLDER_FOR))

# %% Step 2: Sorting rules
def category(path):
    return FOLDER_FOR.get(path.suffix.lower(), "Other")


def should_sort(path):
    return (path.is_file() and not path.name.startswith(".")
            and path.suffix.lower() not in SKIP)


for name in ["scan.PDF", "README", "setup.part", ".DS_Store"]:
    path = downloads / name
    print(f"{name:<11} {category(path):<10} {should_sort(path)}")

# %% Step 3: Planning the moves
def plan(folder):
    """Yield (file, destination) pairs, without moving anything."""
    for path in sorted(folder.iterdir()):
        if should_sort(path):
            yield path, folder / category(path) / path.name


for source, target in plan(downloads):
    print(f"{source.name:<12} -> {target.parent.name}/")

# %% Step 4: Never overwrite a file
from itertools import count


def free_name(target):
    """Return target, or 'name (2).ext' and so on if it is taken."""
    if not target.exists():
        return target
    for n in count(2):
        candidate = target.with_name(
            f"{target.stem} ({n}){target.suffix}")
        if not candidate.exists():
            return candidate

# %% Step 5: Moving files, with a journal
import json

JOURNAL = ".organizer-journal.json"


def organize(folder):
    moves = []
    for source, target in plan(folder):
        target.parent.mkdir(exist_ok=True)
        target = source.move(free_name(target))
        moves.append([str(source), str(target)])
    (folder / JOURNAL).write_text(json.dumps(moves, indent=2))
    return moves

# %% Step 5: Moving files, with a journal
def main(folder):
    moves = list(plan(folder))
    if not moves:
        print("Nothing to sort.")
        return
    print(f"{len(moves)} files will be moved into folders.")
    if input("Go ahead? (y/n) ").strip().lower() != "y":
        print("Nothing was moved.")
        return
    print(f"Moved {len(organize(folder))} files.")

# %% Step 5: Moving files, with a journal
main(downloads)
for sub in sorted(downloads.iterdir()):
    if sub.is_dir():
        names = ", ".join(sorted(p.name for p in sub.iterdir()))
        print(f"  {sub.name + '/':<14}{names}")

# %% Step 5: Moving files, with a journal
docs = downloads / "Documents"
print(free_name(docs / "notes.txt").name)
print(free_name(docs / "todo.txt").name)

# %% Step 6: A report
from collections import Counter


def report(folder):
    sizes, counts = Counter(), Counter()
    for path in folder.rglob("*"):
        if path.is_file() and not path.name.startswith("."):
            sizes[path.parent.name] += path.stat().st_size
            counts[path.parent.name] += 1
    print(f"{'Folder':<13}{'Files':>5}{'Size':>11}")
    for name, size in sizes.most_common():
        mb = size / 1024 ** 2
        print(f"{name:<13}{counts[name]:>5}{mb:8.2f} MB")


report(downloads)

# %% Step 7: Undo
def undo(folder):
    journal = folder / JOURNAL
    moves = json.loads(journal.read_text())
    for source, target in reversed(moves):
        Path(target).move(source)
    journal.unlink()
    for sub in list(folder.iterdir()):
        if sub.is_dir() and not any(sub.iterdir()):
            sub.rmdir()
    return len(moves)


print("Moved back:", undo(downloads))
names = sorted(p.name for p in downloads.iterdir())
print(len(names), "entries, all files:",
      all((downloads / n).is_file() for n in names))
