"""Add up prime numbers: the worker for sum_primes_parallel.py."""


def is_prime(n):
    """Return True if n is a prime number."""
    if n < 2:
        return False
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False
    return True


def sum_primes(start, stop):
    """Return the sum of the primes in range(start, stop)."""
    return sum(n for n in range(start, stop) if is_prime(n))
