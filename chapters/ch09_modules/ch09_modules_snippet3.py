"""Code from "9.7 Writing your own modules" that is shown in the book but not run automatically:
it needs your own data, a server or extra setup. See the book for details."""

if __name__ == "__main__":
    for c in (-40, 0, 37, 100):
        print(f"{c:>4} °C = {c_to_f(c):6.1f} °F")
