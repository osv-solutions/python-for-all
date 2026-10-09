"""Code from "9.4 Randomness: random and secrets" that is shown in the book but not run on its own:
it needs your own data, a server or extra setup, or it is one step of an example
that the book builds up gradually. See the book for details."""

import secrets

print(secrets.randbelow(1_000_000))  # a six-digit-or-less code
print(secrets.token_hex(8))          # 16 random hexadecimal digits
print(secrets.choice("ABCDEFGH"))    # a secure random choice
