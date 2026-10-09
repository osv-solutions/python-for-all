"""Solutions to the Chapter 13 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch13_solutions.py

The explanations are in ch13_solutions.md."""

# %% Exercise 13.1
class Shape:
    def area(self):
        raise NotImplementedError("subclasses must provide area()")

    def describe(self):
        return f"a shape with area {self.area():.2f}"

# %% Exercise 13.1
import math

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

# %% Exercise 13.1
shapes = [Square(3), Circle(1), Square(1.5), Circle(2)]
for shape in shapes:
    print(f"{type(shape).__name__:<7}{shape.describe()}")
try:
    Shape().describe()
except NotImplementedError as err:
    print("Plain shape:", err)

# %% Exercise 13.2
import math
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

    def distance_to(self, other):
        dx, dy = self.x - other.x, self.y - other.y
        return math.sqrt(dx ** 2 + dy ** 2)

a, b = Point(0, 0), Point(3, 4)
print(a, b, a.distance_to(b))
print(Point(3, 4) == b, Point(3, 4) is b, a == b)

# %% Exercise 13.3
class OutOfStock(LookupError):
    """Raised when a shop can't supply the quantity requested."""

    def __init__(self, product, requested, available):
        super().__init__(f"{product}: {requested} requested, "
                         f"{available} in stock")
        self.product = product
        self.requested = requested

# %% Exercise 13.3
class Shop:
    def __init__(self, stock):
        self.stock = dict(stock)      # a copy: name -> quantity

    def sell(self, name, quantity):
        available = self.stock.get(name, 0)
        if quantity > available:
            raise OutOfStock(name, quantity, available)
        self.stock[name] = available - quantity

# %% Exercise 13.3
shop = Shop({"apples": 10, "pears": 2})
shop.sell("apples", 4)
for name, quantity in [("pears", 5), ("kiwis", 1)]:
    try:
        shop.sell(name, quantity)
    except OutOfStock as err:
        print("Sorry:", err)
        print("  wanted", err.requested, "of", err.product)
try:
    shop.sell("apples", 7)
except LookupError as err:
    print(type(err).__name__, "caught as LookupError:", err)
print(shop.stock)

# %% Exercise 13.4
# Setup: recreates the context these solutions build on (from the chapter).
class Money:
    def __init__(self, cents):
        self.cents = cents

    def __repr__(self):
        return f"Money(${self.cents / 100:.2f})"

    def __add__(self, other):
        return Money(self.cents + other.cents)

    def __eq__(self, other):
        return self.cents == other.cents

    def __lt__(self, other):
        return self.cents < other.cents

# %% Exercise 13.4
def __sub__(self, other):
    return Money(self.cents - other.cents)

def __mul__(self, times):
    if not isinstance(times, int):
        raise TypeError("Money can only be multiplied by an int")
    return Money(self.cents * times)

def __str__(self):
    return f"${self.cents / 100:.2f}"

Money.__sub__, Money.__mul__ = __sub__, __mul__
Money.__str__ = __str__

# %% Exercise 13.4
print(Money(1250) * 3 - Money(500))
print([Money(1250) * 3 - Money(500)])
for factor in [1.5, "3"]:
    try:
        print(Money(100) * factor)
    except TypeError as err:
        print("Refused:", err)

# %% Exercise 13.5
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    grades: list[int] = field(default_factory=list)

    @property
    def average(self):
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

# %% Exercise 13.5
def by_average(student):
    return student.average

students = [Student("Asha", [88, 92, 79]), Student("Ben", [65, 70]),
            Student("Chen", [95, 91, 98]), Student("Dina")]
students[3].grades.append(81)
for s in sorted(students, key=by_average, reverse=True):
    print(f"{s.name:<6}{s.average:>6.1f}  {s.grades}")

# %% Exercise 13.6
# Setup: recreates the context these solutions build on (from the chapter).
@dataclass
class Book:
    title: str
    author: str
    pages: int = 0

# %% Exercise 13.6
def describe(value):
    match value:
        case int():
            return f"the whole number {value}"
        case str():
            return f"the text {value!r}"
        case Book(title=t, pages=p) if p > 500:
            return f"a long book: {t}, {p} pages"
        case Book(title=t):
            return f"a book: {t}"
        case _:
            return f"something else: {value!r}"

# %% Exercise 13.6
values = [42, "hello", Book("Dune", "Frank Herbert", 688),
          Book("Emma", "Jane Austen", 474), 3.5, [1, 2], True]
for value in values:
    print(describe(value))

# %% Exercise 13.7
class AlreadyEnrolled(ValueError):
    """Raised when a student is enrolled in a course twice."""

@dataclass
class Course:
    name: str
    students: list[Student] = field(default_factory=list)

    def enroll(self, student):
        for s in self.students:
            if s.name == student.name:
                raise AlreadyEnrolled(f"{s.name} already takes "
                                      f"{self.name}")
        self.students.append(student)

# %% Exercise 13.7
@dataclass
class School:
    name: str
    courses: dict[str, Course] = field(default_factory=dict)

    def add_course(self, name):
        self.courses[name] = Course(name)

    def enroll(self, course_name, student):
        self.courses[course_name].enroll(student)

    def courses_of(self, student_name):
        taken = []
        for course in self.courses.values():
            if any(s.name == student_name for s in course.students):
                taken.append(course.name)
        return taken

# %% Exercise 13.7
school = School("Hillside High")
for name in ["Math", "Art", "Physics"]:
    school.add_course(name)
asha, ben = Student("Asha"), Student("Ben")
school.enroll("Math", asha)
school.enroll("Physics", asha)
school.enroll("Math", ben)
school.enroll("Art", ben)
try:
    school.enroll("Math", Student("Asha", [90]))
except AlreadyEnrolled as err:
    print("Refused:", err)
for student in [asha, ben]:
    print(student.name, "takes", school.courses_of(student.name))
print("Math has", len(school.courses["Math"].students), "students")
