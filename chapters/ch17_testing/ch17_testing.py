"""Chapter 17: Testing Your Code with pytest

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch17_testing.py

or open the notebook and run the cells in order.
"""

# %% 17.2 Checking with assert
def average(numbers):
    return sum(numbers) / len(numbers)

assert average([2, 4, 6]) == 4
assert average([5]) == 5
assert average([-1, 1]) == 0
print("all checks passed")

# %% 17.2 Checking with assert
# This example stops with an error on purpose (see the book).
try:
    assert average([1, 2]) == 2, "average of 1 and 2"
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% 17.2 Checking with assert
def test_average_of_three():
    assert average([2, 4, 6]) == 4

def test_average_of_one():
    assert average([5]) == 5

for test in [test_average_of_three, test_average_of_one]:
    test()
    print(test.__name__, "passed")

# %% 17.7 Comparing floats with pytest.approx
share = (48.5 + 48.5 * 20 / 100) / 3
print(share)
print(share == 19.4)
