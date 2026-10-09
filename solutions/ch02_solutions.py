"""Solutions to the Chapter 2 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch02_solutions.py

The explanations are in ch02_solutions.md."""

# %% Exercise 2.1
print(9 / 3, type(9 / 3))
print(9 // 2, type(9 // 2))
print(9 % 4, type(9 % 4))
print(2 ** 0.5, type(2 ** 0.5))
print("9" * 3, type("9" * 3))
print(int("9") * 3, type(int("9") * 3))

# %% Exercise 2.2
grams_per_batch = 250
batches = 6
total_kg = batches * grams_per_batch / 1000
print(f"{batches} batches need {total_kg} kg of flour.")

# %% Exercise 2.3
celsius = float(input("Temperature in °C: "))
fahrenheit = celsius * 9 / 5 + 32
print(f"{celsius} °C is {fahrenheit} °F")

# %% Exercise 2.3
celsius = float(input("Temperature in °C: "))
fahrenheit = celsius * 9 / 5 + 32
print(f"{celsius} °C is {fahrenheit} °F")

# %% Exercise 2.4
total = int(input("Number of seconds: "))
hours = total // 3600
minutes = total % 3600 // 60
seconds = total % 60
print(f"{hours} h {minutes} min {seconds} s")

# %% Exercise 2.5
a = 5
b = 8
temp = a
a = b
b = temp
print(a, b)
a, b = b, a
print(a, b)

# %% Exercise 2.6
bill = float(input("Bill amount: $"))
tip_percent = int(input("Tip (%): "))
people = int(input("Number of people: "))
total = bill * (1 + tip_percent / 100)
share = total / people
rounded = -(-share // 1)
extra = rounded * people - total
print(f"Exact share: ${share:.2f}, rounded up: ${rounded:.2f}")
print(f"Extra tip in total: ${extra:.2f}")
