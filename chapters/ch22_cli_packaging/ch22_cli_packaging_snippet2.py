"""Code from "22.3 Exit codes and standard error" that is shown in the book but not run on its own:
it needs your own data, a server or extra setup, or it is one step of an example
that the book builds up gradually. See the book for details."""

def main(argv=None):
    args = build_parser().parse_args(argv)
    ...                  # do the work, print the results
    return 0


if __name__ == "__main__":
    sys.exit(main())
