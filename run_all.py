"""Run every script in the companion repository and report the ones that fail.

Scripts that ask for keyboard input are fed the answers used in the book,
from the matching <name>.inputs.txt file.

Usage:  python run_all.py            (all scripts)
        python run_all.py ch03       (only scripts whose path contains "ch03")
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent


def scripts(pattern=""):
    for folder in ("chapters", "projects", "solutions"):
        for path in sorted((ROOT / folder).rglob("*.py")):
            if "_snippet" in path.name or pattern not in str(path):
                continue
            yield path


def run(path):
    inputs = path.with_suffix(".inputs.txt")
    stdin = inputs.read_text(encoding="utf-8") if inputs.exists() else ""
    result = subprocess.run([sys.executable, path.name], cwd=path.parent,
                            input=stdin, capture_output=True, text=True,
                            timeout=300)
    return result.returncode, result.stderr


def main():
    pattern = sys.argv[1] if len(sys.argv) > 1 else ""
    failed = []
    for path in scripts(pattern):
        code, err = run(path)
        name = path.relative_to(ROOT)
        print(f"{'ok  ' if code == 0 else 'FAIL'} {name}")
        if code != 0:
            failed.append((name, err))
    for name, err in failed:
        print(f"\n--- {name}\n{err[-2000:]}")
    print(f"\n{len(failed)} failed" if failed else "\nAll scripts ran successfully.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
