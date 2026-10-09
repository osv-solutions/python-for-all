"""Project 3 (Beginner): Password Generator and Strength Checker

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python p03_passwords.py

The script asks you to type answers. To replay the answers used
in the book instead:

    python p03_passwords.py < p03_passwords.inputs.txt

You can also open the notebook and run the cells in order.
"""

# %% Step 1: What makes a password strong?
import math

alphabets = {"digits only": 10, "lowercase": 26,
             "upper + lower": 52, "letters + digits + symbols": 94}
for name, size in alphabets.items():
    combos = size ** 12
    bits = 12 * math.log2(size)
    print(f"{name:<27} {combos:9.2e} combinations  {bits:5.1f} bits")

# %% Step 1: What makes a password strong?
GUESSES_PER_SECOND = 10_000_000_000   # an assumption for illustration

def years_to_guess(bits):
    """Average years to find a password: half of all combinations."""
    seconds = 2 ** bits / 2 / GUESSES_PER_SECOND
    return seconds / (365.25 * 24 * 3600)

for bits in (40, 60, 80):
    print(f"{bits} bits: {years_to_guess(bits):,.4g} years")

# %% Step 2: Generate a random password
import secrets
import string

print(string.ascii_lowercase)
print(string.digits, string.punctuation)
alphabet = string.ascii_letters + string.digits + string.punctuation
print(len(alphabet), "characters to choose from")
password = ""
for _ in range(16):
    password += secrets.choice(alphabet)
print(password)

# %% Step 3: Guarantee every kind of character
GROUPS = [string.ascii_lowercase, string.ascii_uppercase,
          string.digits, string.punctuation]

def generate(length=16):
    """Return a random password with at least one of each group."""
    if length < len(GROUPS):
        raise ValueError(f"length must be at least {len(GROUPS)}")
    chars = [secrets.choice(group) for group in GROUPS]
    while len(chars) < length:
        chars.append(secrets.choice("".join(GROUPS)))
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)

for length in (12, 16, 24):
    print(length, generate(length))

# %% Step 4: Memorable passphrases
WORDS = """apple badge candle dragon eagle fabric garden harbor island
jungle kettle ladder magnet needle orbit parrot quartz rocket salad
tunnel umbrella velvet walnut yogurt zebra anchor bridge cactus
dolphin engine forest galaxy hammer igloo jacket koala lemon mosaic
""".split()

def passphrase(n_words=5, sep="-"):
    """Return n_words random words joined by sep."""
    return sep.join(secrets.choice(WORDS) for _ in range(n_words))

print(len(WORDS), "words")
print(passphrase())
print(f"{5 * math.log2(len(WORDS)):.1f} bits for 5 words")

# %% Step 5: Check a password's strength
COMMON = {"password", "123456", "123456789", "qwerty", "letmein",
          "password123", "iloveyou", "admin", "welcome", "abc123"}

def alphabet_size(password):
    """Return the size of the alphabet the password draws from."""
    size = 0
    for group in GROUPS:
        for ch in password:
            if ch in group:
                size += len(group)
                break
    return size

# %% Step 5: Check a password's strength
def check(password):
    """Return a rating, an entropy estimate and a list of problems."""
    problems = []
    if password.lower() in COMMON:
        return "very weak", 0.0, ["it is a well-known password"]
    if len(password) < 12:
        problems.append("use at least 12 characters")
    if alphabet_size(password) < 62:
        problems.append("mix capitals, small letters and digits")
    if len(set(password)) < len(password) / 2:
        problems.append("too many repeated characters")
    bits = len(password) * math.log2(max(alphabet_size(password), 2))
    rating = ("strong" if bits >= 70
              else "fair" if bits >= 50 else "weak")
    return rating, bits, problems

# %% Step 5: Check a password's strength
tests = ["Password123", "summer", "Tr0ub4dor&3",
         "kettle-orbit-salad-zebra"]
for pw in tests:
    rating, bits, problems = check(pw)
    print(f"{pw:<25}{rating:<10}{bits:5.1f} bits")
    for problem in problems:
        print(" " * 25, "-", problem)

# %% Step 6: The menu
def main():
    while True:
        menu = "\n[g]enerate, [p]assphrase, [c]heck, [q]uit: "
        match input(menu).strip().lower():
            case "g":
                print("Password:", generate(16))
            case "p":
                print("Passphrase:", passphrase(6))
            case "c":
                pw = input("Password to check: ")
                rating, bits, problems = check(pw)
                print(f"{rating} ({bits:.0f} bits)")
                for problem in problems:
                    print(" -", problem)
            case "q":
                break

# %% Step 6: The menu
main()
