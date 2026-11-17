"""
result_card_generator.py
Task 1 - Student Result Card Generator
Topics: functions (def, parameters, return) and string manipulation.

The program asks for one student's name, roll number and marks in five
subjects, validates every input, grades the student and prints a formatted
result card.
"""

import textwrap

# ---------------------------------------------------------------------------
# Constants (no magic numbers inside the functions)
# ---------------------------------------------------------------------------
SUBJECTS = ["English", "Mathematics", "Science", "Computer Science", "Social Studies"]
MIN_MARKS = 0                 # lowest mark allowed for a subject
MAX_MARKS = 100               # highest mark allowed for a subject
SUBJECT_PASS_MARK = 40        # any subject below this forces a Fail result
FAIL_GRADE = "Fail"
# (minimum percentage, grade) checked from the top down
GRADE_BANDS = [(90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D")]
CARD_WIDTH = 44               # width of the printed result card
NAME_SPECIAL_CHARS = " .'-"   # non-letter characters allowed inside a name


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


def format_name(name):
    """Clean a name: strip outer spaces, collapse inner spaces, apply title case."""
    return " ".join(name.strip().split()).title()


def get_valid_name():
    """Ask for the student's name until a non-empty, letters-only name is entered."""
    while True:
        name = format_name(input("Enter student name: "))
        # every character must be a letter or an allowed symbol, with >= 1 letter
        only_valid_chars = all(ch.isalpha() or ch in NAME_SPECIAL_CHARS for ch in name)
        if name and only_valid_chars and any(ch.isalpha() for ch in name):
            return name
        print("  Invalid name: use letters (and spaces, . ' -) only. Please try again.")


def get_valid_roll_number():
    """Ask for the roll number until it contains digits only (checked with isdigit)."""
    while True:
        roll_number = input("Enter roll number: ").strip()
        # isascii() blocks characters such as superscript digits that isdigit() accepts
        if roll_number.isdigit() and roll_number.isascii():
            return roll_number          # kept as text so leading zeros are not lost
        print("  Invalid roll number: digits only (0-9). Please try again.")


def get_valid_marks(subject):
    """Ask for one subject's marks until a whole number from 0 to 100 is entered."""
    while True:
        raw_value = input(f"Enter marks for {subject} ({MIN_MARKS}-{MAX_MARKS}): ").strip()
        marks = parse_whole_number(raw_value)
        if marks is None:
            print(f"  Invalid input: '{raw_value}' is not a whole number. Please try again.")
        elif MIN_MARKS <= marks <= MAX_MARKS:
            return marks
        else:
            print(f"  Invalid marks: {marks} is outside {MIN_MARKS}-{MAX_MARKS}. Please try again.")


# ---------------------------------------------------------------------------
# Calculation helpers
# ---------------------------------------------------------------------------
def calculate_percentage(total, max_total):
    """Return the percentage (rounded to 2 decimals) of total out of max_total."""
    if max_total <= 0:
        raise ValueError("max_total must be greater than zero")
    return round(total / max_total * 100, 2)


def get_grade(percentage):
    """Return the letter grade for a percentage using the GRADE_BANDS table."""
    if not 0 <= percentage <= 100:
        raise ValueError("percentage must be between 0 and 100")
    for minimum, grade in GRADE_BANDS:
        if percentage >= minimum:
            return grade
    return FAIL_GRADE                    # below the lowest band (under 50)


def get_failed_subjects(marks_by_subject):
    """Return the names of subjects where marks are below the subject pass mark."""
    return [subject for subject, marks in marks_by_subject.items()
            if marks < SUBJECT_PASS_MARK]


def get_final_result(percentage, failed_subjects):
    """Return (grade, status); one failed subject makes the result Fail."""
    grade = get_grade(percentage)
    if failed_subjects:                  # the "below 40" rule beats the percentage
        grade = FAIL_GRADE
    status = "Fail" if grade == FAIL_GRADE else "Pass"
    return grade, status


def get_fail_reasons(percentage, failed_subjects):
    """Return sentences explaining why the student failed (empty list if passed)."""
    reasons = []
    if failed_subjects:
        reasons.append(f"Marks below {SUBJECT_PASS_MARK} in: {', '.join(failed_subjects)}.")
    if get_grade(percentage) == FAIL_GRADE:
        reasons.append(f"Overall percentage is below {GRADE_BANDS[-1][0]}%.")
    return reasons


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
def build_result_card(name, roll_number, marks_by_subject, total, max_total,
                      percentage, grade, status, reasons):
    """Build the formatted result card (f-strings) and return it as one string."""
    border = "=" * CARD_WIDTH
    divider = "-" * CARD_WIDTH
    lines = [
        border,
        f"{'STUDENT RESULT CARD':^{CARD_WIDTH}}",
        border,
        f"{'Name':<14}: {name}",
        f"{'Roll Number':<14}: {roll_number}",
        divider,
        f"{'Subject':<22}{'Marks':>10}{'Status':>12}",
        divider,
    ]
    for subject, marks in marks_by_subject.items():
        score_text = f"{marks}/{MAX_MARKS}"
        subject_status = "Fail" if marks < SUBJECT_PASS_MARK else "Pass"
        lines.append(f"{subject:<22}{score_text:>10}{subject_status:>12}")
    lines += [
        divider,
        f"{'Total Marks':<14}: {total} / {max_total}",
        f"{'Percentage':<14}: {percentage:.2f}%",
        f"{'Grade':<14}: {grade}",
        f"{'Final Status':<14}: {status}",
    ]
    if reasons:
        lines.append(divider)
        lines.append("Remarks:")
        for reason in reasons:
            lines.append(textwrap.fill(f"* {reason}", width=CARD_WIDTH,
                                       subsequent_indent="  "))
    lines.append(border)
    return "\n".join(lines)


def main():
    """Collect the input, process it and print the result card."""
    print("=== Student Result Card Generator ===")
    name = get_valid_name()
    roll_number = get_valid_roll_number()

    marks_by_subject = {}
    for subject in SUBJECTS:
        marks_by_subject[subject] = get_valid_marks(subject)

    total = sum(marks_by_subject.values())
    max_total = MAX_MARKS * len(SUBJECTS)
    percentage = calculate_percentage(total, max_total)
    failed_subjects = get_failed_subjects(marks_by_subject)
    grade, status = get_final_result(percentage, failed_subjects)
    reasons = get_fail_reasons(percentage, failed_subjects)

    print()
    print(build_result_card(name, roll_number, marks_by_subject, total, max_total,
                            percentage, grade, status, reasons))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nInput cancelled. Exiting without a result card.")
