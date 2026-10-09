# Solutions: Chapter 13, Inheritance, Composition and Data Classes

Worked solutions to the exercises at the end of Chapter 13 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch13_solutions.ipynb`](ch13_solutions.ipynb) or the script `ch13_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 13.1

*Write a base class `Shape` with a method `describe()` that uses an `area()` method provided by subclasses `Square` and `Circle`, and describe a list of shapes.*

```python
class Shape:
    def area(self):
        raise NotImplementedError("subclasses must provide area()")

    def describe(self):
        return f"a shape with area {self.area():.2f}"
```

`describe` is written once, in the base class, and calls `self.area()` without knowing which kind of shape `self` is. The base class's own `area` raises `NotImplementedError`, a built-in exception meant for exactly this situation: a method that a subclass is supposed to override. Now the two subclasses:

```python
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
```

Each subclass stores its own measurements and overrides `area`. Neither defines `describe`; both inherit it.

```python
shapes = [Square(3), Circle(1), Square(1.5), Circle(2)]
for shape in shapes:
    print(f"{type(shape).__name__:<7}{shape.describe()}")
try:
    Shape().describe()
except NotImplementedError as err:
    print("Plain shape:", err)
```

Output:

```text
Square a shape with area 9.00
Circle a shape with area 3.14
Square a shape with area 2.25
Circle a shape with area 12.57
Plain shape: subclasses must provide area()
```

The same call, `shape.describe()`, gives 9.00 for the first square, 3.14 for the unit circle, 2.25 for the small square and 12.57 for the circle of radius 2. This is polymorphism at work: `describe` calls `self.area()`, and Python finds the `area` of the object's own class. A plain `Shape` has no real area, so describing it raises the exception with our message.

## Exercise 13.2

*Turn `Point` from Chapter 12 into a data class with `x` and `y`, add a method `distance_to(other)`, and check that two points with the same coordinates are equal.*

```python
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
```

Output:

```text
Point(x=0, y=0) Point(x=3, y=4) 5.0
True False False
```

The data class needs only two lines for its attributes; `@dataclass` writes `__init__`, `__repr__` and `__eq__`. The distance uses the Pythagorean theorem: the classic 3-4-5 triangle gives 5.0. A new `Point(3, 4)` is equal to `b`, because the generated `__eq__` compares the attributes, but `is` shows that it is a different object. The Chapter 12 class, without `__eq__`, would have said `False` to `==` as well.

## Exercise 13.3

*Write a custom exception `OutOfStock(LookupError)` that stores the product name and the quantity requested, and raise it from a `Shop` class's `sell(name, quantity)` method.*

```python
class OutOfStock(LookupError):
    """Raised when a shop can't supply the quantity requested."""

    def __init__(self, product, requested, available):
        super().__init__(f"{product}: {requested} requested, "
                         f"{available} in stock")
        self.product = product
        self.requested = requested
```

`LookupError` is the built-in base class of `KeyError` and `IndexError`, a fitting parent for "the thing you asked for isn't there". The exception also receives the quantity available, to build a helpful message, and stores the product and the quantity requested as attributes for code that catches it.

```python
class Shop:
    def __init__(self, stock):
        self.stock = dict(stock)      # a copy: name -> quantity

    def sell(self, name, quantity):
        available = self.stock.get(name, 0)
        if quantity > available:
            raise OutOfStock(name, quantity, available)
        self.stock[name] = available - quantity
```

`get` with a default of 0 treats an unknown product like one that has run out, so a single check covers both. The shop copies the dictionary it is given, so selling never changes the caller's dictionary.

```python
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
```

Output:

```text
Sorry: pears: 5 requested, 2 in stock
  wanted 5 of pears
Sorry: kiwis: 1 requested, 0 in stock
  wanted 1 of kiwis
OutOfStock caught as LookupError: apples: 7 requested, 6 in stock
{'apples': 6, 'pears': 2}
```

Four apples are sold, leaving 6. Five pears are more than the 2 in stock, and kiwis aren't stocked at all, so both raise `OutOfStock`, whose attributes the handler reads. The last attempt, 7 apples, is caught by `except LookupError`, because an `OutOfStock` *is a* `LookupError`. The final stock shows 6 apples and 2 pears: refused sales change nothing.

## Exercise 13.4

*Give `Money` the special methods `__sub__`, `__mul__` and `__str__`, so that `print(Money(1250) * 3 - Money(500))` prints `$32.50`.*

<details>
<summary>Setup code: recreates the data and helpers from the chapter (click to show)</summary>

```python
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
```

</details>

The `Money` class from the chapter is set up first. With three more methods, the class would no longer fit in one short listing, so, as in the solutions to Chapter 12, the new methods are written as functions and then stored in the class. In your own file, put them inside the class:

```python
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
```

Like `__add__`, the two arithmetic methods return a *new* `Money` object and never change the original. `__mul__` checks that it got a whole number: multiplying an amount of money by 1.5 would give fractions of a cent. `__str__` gives the friendly text for `print`, while `__repr__` keeps the more precise form.

```python
print(Money(1250) * 3 - Money(500))
print([Money(1250) * 3 - Money(500)])
for factor in [1.5, "3"]:
    try:
        print(Money(100) * factor)
    except TypeError as err:
        print("Refused:", err)
```

Output:

```text
$32.50
[Money($32.50)]
Refused: Money can only be multiplied by an int
Refused: Money can only be multiplied by an int
```

`Money(1250) * 3` calls `__mul__` and gives $37.50, and subtracting $5.00 with `__sub__` leaves `$32.50`, as required. Inside a list, the same amount appears as `Money($32.50)`, because lists use `__repr__`. Both 1.5 and the string `"3"` are refused. One limitation remains: `3 * Money(100)` puts the number first, so Python asks the number to do the multiplication, which needs another special method, `__rmul__`.

## Exercise 13.5

*Write a data class `Student` with a name and a list of grades, using `default_factory`, and a property `average`. Sort a list of students by average.*

```python
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
```

`field(default_factory=list)` gives every student a new empty list, so a student created without grades doesn't share a list with anybody else. The property guards against an empty list, which would otherwise cause a `ZeroDivisionError`.

```python
def by_average(student):
    return student.average

students = [Student("Asha", [88, 92, 79]), Student("Ben", [65, 70]),
            Student("Chen", [95, 91, 98]), Student("Dina")]
students[3].grades.append(81)
for s in sorted(students, key=by_average, reverse=True):
    print(f"{s.name:<6}{s.average:>6.1f}  {s.grades}")
```

Output:

```text
Chen    94.7  [95, 91, 98]
Asha    86.3  [88, 92, 79]
Dina    81.0  [81]
Ben     67.5  [65, 70]
```

`key` needs a function that takes one item and returns what to compare (Chapter 8), so `by_average` returns a student's average. Chen comes first with 94.7, then Asha with 86.3, Dina with 81.0 and Ben with 67.5. Dina was created without grades and got one afterward; her list is her own, so nobody else's grades changed. (Chapter 15 shows a shorter way to write a key function like this, with `lambda`.)

## Exercise 13.6

*Use `match` with class patterns to describe a list of mixed values: an `int`, a `str`, a `Book` with more than 500 pages, any other `Book`, and anything else.*

<details>
<summary>Setup code: recreates the data and helpers from the chapter (click to show)</summary>

```python
@dataclass
class Book:
    title: str
    author: str
    pages: int = 0
```

</details>

The `Book` data class from the chapter is set up first.

```python
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
```

`case int():` is a class pattern with empty parentheses, which matches any `int` without pulling out any attributes. The two `Book` cases are in a deliberate order: the one with the guard comes first, because `match` takes the first case that fits, and the plain `Book(title=t)` would match every book. `case _:` catches everything else.

```python
values = [42, "hello", Book("Dune", "Frank Herbert", 688),
          Book("Emma", "Jane Austen", 474), 3.5, [1, 2], True]
for value in values:
    print(describe(value))
```

Output:

```text
the whole number 42
the text 'hello'
a long book: Dune, 688 pages
a book: Emma
something else: 3.5
something else: [1, 2]
the whole number True
```

*Dune*, with 688 pages, is a long book, and *Emma* an ordinary one. The float 3.5 and the list fall through to `case _`. The last line is a surprise: `True` is described as `the whole number True`. In Python, `bool` is a subclass of `int`, so a Boolean *is an* `int`, and the class pattern matches it. A `case bool():` placed before `case int():` would treat Booleans separately.

## Exercise 13.7

*Model a school: a `Course` has a name and a list of `Student` data classes, and a `School` has courses. Add methods to enroll a student, refusing duplicates with a custom exception, and to list every course a student takes.*

```python
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
```

The exception class is just a name and a docstring, inheriting from `ValueError`. `enroll` compares *names* rather than whole `Student` objects: data classes compare all their attributes, so the same student with an extra grade would otherwise count as a different student. The school *has* courses, which it keeps in a dictionary by name:

```python
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
```

`School.enroll` finds the course and hands the work to `Course.enroll`, so the rule against duplicates lives in one place. The hint `dict[str, Course]` says that the keys are names and the values courses. `courses_of` checks each course with `any`, a built-in function that is true when at least one item is true (Chapter 14); here, when at least one student in the course has the given name. This is composition twice over: a school has courses, and a course has students.

```python
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
```

Output:

```text
Refused: Asha already takes Math
Asha takes ['Math', 'Physics']
Ben takes ['Math', 'Art']
Math has 2 students
```

The second enrollment of Asha in Math is refused, even though it is a new `Student` object with a grade, because the names match. Asha takes Math and Physics, Ben takes Math and Art, and Math has 2 students. Enrolling in a course that doesn't exist, such as `school.enroll("Music", asha)`, would raise a `KeyError` from the dictionary lookup.
