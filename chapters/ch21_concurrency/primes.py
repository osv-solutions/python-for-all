"""Count prime numbers: slow, CPU-bound work on purpose."""


def is_prime(n):
    """Return True if n is a prime number."""
    if n < 2:
        return False
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False
    return True


def count_primes(start, stop):
    """Return how many primes are in range(start, stop)."""
    return sum(1 for n in range(start, stop) if is_prime(n))
