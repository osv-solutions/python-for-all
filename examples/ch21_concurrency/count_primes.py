"""Count the primes below one million on all CPU cores."""
from concurrent.futures import ProcessPoolExecutor

from primes import count_primes

STARTS = [0, 250_000, 500_000, 750_000]
STOPS = [250_000, 500_000, 750_000, 1_000_000]

if __name__ == "__main__":
    with ProcessPoolExecutor() as pool:
        counts = list(pool.map(count_primes, STARTS, STOPS))
    for start, count in zip(STARTS, counts):
        print(f"from {start:>7,}: {count:>6,} primes")
    print(f"total below 1,000,000: {sum(counts):,}")
