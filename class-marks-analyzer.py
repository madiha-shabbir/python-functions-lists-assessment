"""
class_marks_analyzer.py
Task 2 - Class Marks Analyzer
Topics: lists (append, len, sum, max, min, sorted) and loops.

The program stores names and marks for a whole class in two parallel lists,
then reports the average, highest/lowest scorers, pass/fail counts, students
above the average and a ranking from highest to lowest marks.
"""

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MIN_MARKS = 0            # lowest mark allowed
MAX_MARKS = 100          # highest mark allowed
PASS_MARK = 50           # 50 or above passes, below 50 fails
REPORT_WIDTH = 52        # width of the report borders


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------
def parse_whole_number(text):
    """Convert text to an int, or return None if it is not a plain whole number."""
    body = text[1:] if text.startswith(("+", "-")) else text
    # isascii() rejects look-alike digits and int() would accept "1_0"
    if body.isascii() and body.isdigit():
        return int(text)
    return None


def clean_name(name):
    """Strip outer spaces, collapse inner spaces and apply title case to a name."""
    return " ".join(name.strip().split()).title()


def get_valid_student_count():
    """Ask how many students are in the class until a number of 1 or more is given."""
    while True:
        raw_value = input("How many students are in the class? ").strip()
        count = parse_whole_number(raw_value)
        if count is None:
            print(f"  Invalid input: '{raw_value}' is not a whole number. Please try again.")
        elif count < 1:
            print("  The class must have at least 1 student. Please try again.")
        else:
            return count


def get_valid_student_name(position):
    """Ask for the name of student number `position` until it is not empty."""
    while True:
        name = clean_name(input(f"Enter name of student {position}: "))
        if name:
            return name
        print("  Name cannot be empty. Please try again.")


def get_valid_mark(student_name):
    """Ask for one student's marks until a whole number from 0 to 100 is entered."""
    while True:
        raw_value = input(f"  Enter marks for {student_name} ({MIN_MARKS}-{MAX_MARKS}): ").strip()
        mark = parse_whole_number(raw_value)
        if mark is None:
            print(f"  Invalid input: '{raw_value}' is not a whole number. Please try again.")
        elif MIN_MARKS <= mark <= MAX_MARKS:
            return mark
        else:
            print(f"  Invalid marks: {mark} is outside {MIN_MARKS}-{MAX_MARKS}. Please try again.")


# ---------------------------------------------------------------------------
# Analysis helpers (custom functions)
# ---------------------------------------------------------------------------
def calculate_average(marks):
    """Return the average of a non-empty list of marks."""
    return sum(marks) / len(marks)


def find_students_with_mark(names, marks, target_mark):
    """Return every student name whose mark equals target_mark (handles ties)."""
    matches = []
    for index in range(len(marks)):
        if marks[index] == target_mark:
            matches.append(names[index])
    return matches


def count_pass_fail(marks):
    """Return (passed, failed): marks of PASS_MARK or above pass, the rest fail."""
    passed = 0
    for mark in marks:
        if mark >= PASS_MARK:
            passed += 1
    return passed, len(marks) - passed


def get_students_above_average(names, marks, average):
    """Return (name, mark) pairs for students scoring strictly above the average."""
    above = []
    for name, mark in zip(names, marks):
        if mark > average:
            above.append((name, mark))
    return above


def get_ranking(names, marks):
    """Return (rank, name, mark) rows from highest to lowest; ties share a rank."""
    # sorting positions (not values) keeps each name attached to its mark;
    # sorted() is stable, so tied students stay in the order they were entered
    order = sorted(range(len(marks)), key=lambda i: marks[i], reverse=True)
    ranking = []
    previous_mark = None
    rank = 0
    for position, index in enumerate(order, start=1):
        if marks[index] != previous_mark:
            rank = position              # new mark -> rank equals position (1, 2, 2, 4)
            previous_mark = marks[index]
        ranking.append((rank, names[index], marks[index]))
    return ranking


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
def print_report(student_names, student_marks):
    """Calculate every statistic and print the complete class report."""
    total_students = len(student_marks)
    average = calculate_average(student_marks)
    highest = max(student_marks)
    lowest = min(student_marks)
    top_students = find_students_with_mark(student_names, student_marks, highest)
    bottom_students = find_students_with_mark(student_names, student_marks, lowest)
    passed, failed = count_pass_fail(student_marks)
    above_average = get_students_above_average(student_names, student_marks, average)
    ranking = get_ranking(student_names, student_marks)

    border = "=" * REPORT_WIDTH
    print(border)
    print(f"{'CLASS PERFORMANCE REPORT':^{REPORT_WIDTH}}")
    print(border)
    print(f"{'Total students':<20}: {total_students}")
    print(f"{'Class average':<20}: {average:.2f}")
    print(f"{'Highest marks':<20}: {highest} -> {', '.join(top_students)}")
    print(f"{'Lowest marks':<20}: {lowest} -> {', '.join(bottom_students)}")
    print(f"{'Passing (>= ' + str(PASS_MARK) + ')':<20}: {passed}")
    print(f"{'Failing (< ' + str(PASS_MARK) + ')':<20}: {failed}")
    print(f"{'Pass rate':<20}: {passed / total_students * 100:.2f}%")

    print(f"\nStudents above the class average ({average:.2f}):")
    if above_average:
        for name, mark in above_average:
            print(f"  - {name}: {mark}")
    else:
        print("  None - no student scored above the class average.")

    print("\nMarks sorted from highest to lowest:")
    print(f"  {sorted(student_marks, reverse=True)}")
    name_width = max(len("Name"), max(len(name) for name in student_names))
    print(f"\n  {'Rank':<6}{'Name':<{name_width + 2}}{'Marks':>5}")
    print(f"  {'-' * (6 + name_width + 2 + 5)}")
    for rank, name, mark in ranking:
        print(f"  {rank:<6}{name:<{name_width + 2}}{mark:>5}")
    print(border)


def main():
    """Collect names and marks into two lists, then print the class report."""
    print("=== Class Marks Analyzer ===")
    class_size = get_valid_student_count()

    student_names = []       # student_names[i] belongs to student_marks[i]
    student_marks = []

    for position in range(1, class_size + 1):
        name = get_valid_student_name(position)
        student_names.append(name)
        student_marks.append(get_valid_mark(name))

    print()
    print_report(student_names, student_marks)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nInput cancelled. Exiting without a report.")
