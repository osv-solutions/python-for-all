# Chapter 21: counting primes on all cores

The process pool example of Chapter 21. `primes.py` holds the worker function,
`count_primes.py` runs it in a `ProcessPoolExecutor`. Only the standard library
is needed. Run it from this folder:

```bash
cd examples/ch21_concurrency
python count_primes.py
```

It prints the number of primes in four ranges and their total, 78,498 primes
below one million. The pool is created under `if __name__ == "__main__":`, and
the worker lives in its own module so that the worker processes can import it.
