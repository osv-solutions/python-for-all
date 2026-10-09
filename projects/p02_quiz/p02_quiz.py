"""Project 2 (Beginner): Quiz Game with Scores

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python p02_quiz.py

The script asks you to type answers. To replay the answers used
in the book instead:

    python p02_quiz.py < p02_quiz.inputs.txt

You can also open the notebook and run the cells in order.
"""

# %% Step 1: Store the questions
questions = [
    {"q": "Which planet is closest to the Sun?",
     "options": ["Venus", "Mercury", "Mars", "Earth"],
     "answer": "Mercury", "category": "Science"},
    {"q": "What is 7 x 8?", "options": ["54", "56", "64", "48"],
     "answer": "56", "category": "Math"},
    {"q": "Which language has the most native speakers?",
     "options": ["English", "Spanish", "Hindi",
                 "Mandarin Chinese"],
     "answer": "Mandarin Chinese", "category": "Geography"},
    {"q": "What does len('quiz') return?",
     "options": ["3", "4", "5", "'quiz'"],
     "answer": "4", "category": "Python"},
    {"q": "Which is a prime number?",
     "options": ["21", "27", "29", "33"],
     "answer": "29", "category": "Math"},
]

# %% Step 1: Store the questions
for item in questions:
    if item["answer"] not in item["options"]:
        print("Bad answer key:", item["q"])
categories = {item["category"] for item in questions}
print(len(questions), "questions in", len(categories), "categories")

# %% Step 2: Ask one question
item = questions[0]
letters = "ABCD"
print(item["q"])
for i, option in enumerate(item["options"]):
    print(f"  {letters[i]}) {option}")
choice = input("Your answer: ").strip().upper()
picked = item["options"][letters.index(choice)]
print("Correct!" if picked == item["answer"] else "Wrong.")

# %% Step 3: Play the whole quiz
import random
random.seed(5)
score, mistakes = 0, []
order = random.sample(questions, len(questions))
for number, item in enumerate(order, start=1):
    print(f"\nQ{number}. {item['q']}")
    options = item["options"]
    for letter, option in zip("ABCD", options):
        print(f"  {letter}) {option}")
    choice = input("Your answer: ").strip().upper()
    while choice not in ("A", "B", "C", "D"):
        choice = input("Please type A, B, C or D: ").strip().upper()
    picked = options["ABCD".index(choice)]
    if picked == item["answer"]:
        score += 1
    else:
        mistakes.append((item, picked))

# %% Step 4: Score by category
asked, right = {}, {}
wrong_questions = [item["q"] for item, picked in mistakes]
for item in questions:
    cat = item["category"]
    asked[cat] = asked.get(cat, 0) + 1
    if item["q"] not in wrong_questions:
        right[cat] = right.get(cat, 0) + 1
for cat in sorted(asked):
    got = right.get(cat, 0)
    bar = "#" * got + "." * (asked[cat] - got)
    print(f"{cat:<10} {got}/{asked[cat]}  {bar}")

# %% Step 5: The final report
percent = score / len(questions)
if percent == 1:
    rating = "Perfect!"
elif percent >= 0.6:
    rating = "Well done."
else:
    rating = "Keep practicing."
print(f"\nScore: {score}/{len(questions)} ({percent:.0%}). {rating}")
for item, picked in mistakes:
    print(f"- {item['q']}")
    print(f"  You said {picked}; the answer is {item['answer']}.")
