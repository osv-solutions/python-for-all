"""Code from "22.1 Arguments on the command line" that is shown in the book but not run on its own:
it needs your own data, a server or extra setup, or it is one step of an example
that the book builds up gradually. See the book for details."""

import sys

print(sys.argv)
print(len(sys.argv) - 1, "arguments")
