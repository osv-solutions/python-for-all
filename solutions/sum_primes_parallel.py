"""Sum the primes below one million in four chunks, in parallel."""
from concurrent.futures import ProcessPoolExecutor

from prime_sums import sum_primes

STARTS = [0, 250_000, 500_000, 750_000]
STOPS = [250_000, 500_000, 750_000, 1_000_000]

if __name__ == "__main__":
    with ProcessPoolExecutor() as pool:
        sums = list(pool.map(sum_primes, STARTS, STOPS))
    for start, stop, total in zip(STARTS, STOPS, sums):
        print(f"{start:>7,} to {stop:>9,}: {total:>15,}")
    print(f"all primes below 1,000,000: {sum(sums):,}")
