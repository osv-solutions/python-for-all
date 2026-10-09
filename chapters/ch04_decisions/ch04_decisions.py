"""Chapter 4: Making Decisions

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch04_decisions.py

The script asks you to type answers. To replay the answers used
in the book instead:

    python ch04_decisions.py < ch04_decisions.inputs.txt

You can also open the notebook and run the cells in order.
"""

# %% 4.1 Comparing values
temperature = 31
print(temperature > 30)
print(temperature == 30, temperature != 30)
is_hot = temperature >= 30
print(is_hot, type(is_hot))

# %% 4.1 Comparing values
print("apple" == "Apple", "apple" == "apple")
print("apple" < "banana", "cherry" < "banana")
print("Zebra" < "apple", "10" < "9")
print(5 == "5", 3 == 3.0)

# %% 4.2 The if statement
temperature = 31
if temperature > 30:
    print("It's hot today.")
    print("Remember to drink water.")
print("Have a nice day!")

# %% 4.2 The if statement
# This example contains a mistake on purpose (see the book).
# Python would refuse to run this whole file, so it is commented
# out. Copy it into a file of its own to see the error message:
# x = 5
# if x == 5
#     print("five")


# %% 4.2 The if statement
# This example contains a mistake on purpose (see the book).
# Python would refuse to run this whole file, so it is commented
# out. Copy it into a file of its own to see the error message:
# x = 5
# if x == 5:
# print("five")


# %% 4.3 Choosing between two paths: else
number = int(input("Enter a whole number: "))
if number % 2 == 0:
    print(number, "is even.")
else:
    print(number, "is odd.")

# %% 4.4 Choosing between many paths: elif
score = 78
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"
print(f"A score of {score} earns a {grade}.")

# %% 4.4 Choosing between many paths: elif
score = 95
if score >= 60:
    grade = "D"
elif score >= 90:
    grade = "A"
else:
    grade = "F"
print(grade)

# %% 4.5 Combining conditions: and, or, not
age = 70
has_ticket = True
print(age < 12 or age >= 65)
print(age >= 18 and has_ticket)
print(not has_ticket)
print(13 <= age <= 19)

# %% 4.5 Combining conditions: and, or, not
day = "Saturday"
hour = 10
is_weekend = day == "Saturday" or day == "Sunday"
if is_weekend and (hour < 8 or hour > 22):
    print("Quiet hours: please keep it down.")
elif is_weekend:
    print("Enjoy your weekend!")
else:
    print("Have a good working day.")

# %% 4.6 Truthiness
print(bool(""), bool(" "), bool("False"))
print(bool(0), bool(0.0), bool(42), bool(None))

# %% 4.6 Truthiness
name = input("Your name (optional): ").strip()
if name:
    print(f"Welcome, {name}!")
else:
    print("Welcome, guest!")

# %% 4.7 Nested decisions
answer = input("How many tickets? ")
if answer.isdigit():
    tickets = int(answer)
    if tickets == 0:
        print("No tickets? Maybe next time.")
    else:
        print(f"That will be ${tickets * 15}.")
else:
    print(f"Sorry, {answer!r} is not a whole number.")

# %% 4.7 Nested decisions
answer = input("How many tickets? ")
if not answer.isdigit():
    print(f"Sorry, {answer!r} is not a whole number.")
elif int(answer) == 0:
    print("No tickets? Maybe next time.")
else:
    print(f"That will be ${int(answer) * 15}.")

# %% 4.8 Conditional expressions
age = 15
ticket = "child" if age < 16 else "adult"
print(ticket)
points = 1
print(f"You scored {points} point{'s' if points != 1 else ''}.")

# %% 4.9 The match statement
command = input("Command: ").strip().lower()
match command:
    case "start":
        print("Starting the game...")
    case "help" | "?":
        print("Commands: start, help, quit")
    case "quit" | "exit":
        print("Goodbye!")
    case _:
        print(f"Unknown command: {command}")

# %% 4.10 Putting it together: a ticket machine
answer = input("Your age: ").strip()
if not answer.isdigit():
    print("Please enter your age in whole years.")
else:
    age = int(answer)
    if age < 5:
        price = 0
    elif age < 18 or age >= 65:
        price = 8
    else:
        price = 15
    day = input("Day of your visit: ").strip().lower()
    match day:
        case "tuesday":
            price = price / 2
    print(f"Ticket price: ${price:.2f}")
