"""Solutions to the Chapter 4 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch04_solutions.py

The explanations are in ch04_solutions.md."""

# %% Exercise 4.1
print(7 >= 7, "cat" < "dog", "Cat" == "cat")
print(not (3 > 2), 5 < 3 or 2 < 4, 1 <= 0.5 <= 2)
print(bool("0"))

# %% Exercise 4.2
number = float(input("A number: "))
if number > 0:
    print("positive")
elif number < 0:
    print("negative")
else:
    print("zero")

# %% Exercise 4.3
year = int(input("Year: "))
if year % 400 == 0:
    print(year, "is a leap year.")
elif year % 100 == 0:
    print(year, "is not a leap year.")
elif year % 4 == 0:
    print(year, "is a leap year.")
else:
    print(year, "is not a leap year.")

# %% Exercise 4.3
for year in (2024, 1900, 2000, 2026):
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    print(year, leap)

# %% Exercise 4.4
weight = float(input("Weight (kg): "))
height = float(input("Height (m): "))
bmi = weight / height ** 2
if bmi < 18.5:
    category = "underweight"
elif bmi < 25:
    category = "normal"
elif bmi < 30:
    category = "overweight"
else:
    category = "obese"
print(f"BMI {bmi:.1f}: {category}")

# %% Exercise 4.5
password = input("New password: ")
ok = True
if len(password) < 8:
    print("- It must have at least 8 characters.")
    ok = False
if password.lower() == password:
    print("- It must contain a capital letter.")
    ok = False
if "password" in password.lower():
    print('- It must not contain the word "password".')
    ok = False
if ok:
    print("Password accepted.")

# %% Exercise 4.6
age = int(input("Your age: "))
if age < 5:
    price = 0
elif age < 18 or age >= 65:
    price = 8
else:
    price = 15
day = input("Day of your visit: ").strip().lower()
match day:
    case "monday":
        print("Sorry, the museum is closed on Mondays.")
    case "tuesday":
        print(f"Ticket price: ${price / 2:.2f}")
    case "sunday":
        print(f"Ticket price: ${price + 2:.2f}")
    case _:
        print(f"Ticket price: ${price:.2f}")

# %% Exercise 4.7
p1 = input("Player 1 (rock, paper, scissors): ").strip().lower()
p2 = input("Player 2 (rock, paper, scissors): ").strip().lower()
valid = ("rock", "paper", "scissors")
if p1 not in valid or p2 not in valid:
    print("Both players must choose rock, paper or scissors.")
elif p1 == p2:
    print("A draw!")
elif (p1 == "rock" and p2 == "scissors"
      or p1 == "scissors" and p2 == "paper"
      or p1 == "paper" and p2 == "rock"):
    print("Player 1 wins!")
else:
    print("Player 2 wins!")
