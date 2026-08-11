students = [
    {"name": "Ali", "marks": [78, 65, 32, 90, 55]},
    {"name": "Ahmed", "marks": [90, 85, 76, 88, 95]},
    {"name": "Sara", "marks": [45, 67, 89, 34, 72]},
    {"name": "Hassan", "marks": [55, 48, 62, 71, 59]},
    {"name": "Ayesha", "marks": [92, 88, 95, 90, 87]},
    {"name": "Usman", "marks": [35, 42, 38, 50, 44]},
    {"name": "Fatima", "marks": [70, 75, 68, 82, 79]},
    {"name": "Bilal", "marks": [60, 55, 73, 48, 66]},
    {"name": "Zainab", "marks": [85, 91, 78, 88, 94]},
    {"name": "Hamza", "marks": [40, 52, 37, 65, 58]}
]


def generate_result(name, passing_marks=40, bonus=5):

    for student in students:

        if student["name"] == name:

            marks = student["marks"]


            final_marks = []

            for mark in marks:
                new_mark = mark + bonus
                if new_mark > 100:
                    new_mark = 100

                final_marks.append(new_mark)


            total = sum(final_marks)

            average = total / len(final_marks)


            highest = max(final_marks)
            lowest = min(final_marks)


            passed = 0
            failed = 0

            for mark in final_marks:

                if mark >= passing_marks:
                    passed += 1
                else:
                    failed += 1

           
            if failed == 0:
                result = "PASS"
            else:
                result = "FAIL"

            # Grade
            if average >= 90:
                grade = "A+"
            elif average >= 80:
                grade = "A"
            elif average >= 70:
                grade = "B"
            elif average >= 60:
                grade = "C"
            elif average >= 50:
                grade = "D"
            else:
                grade = "F"

            return {
                "name": name,
                "marks": final_marks,
                "total": total,
                "average": average,
                "highest": highest,
                "lowest": lowest,
                "passed": passed,
                "failed": failed,
                "grade": grade,
                "result": result
            }

    return None



result = generate_result("Ali")

if result:
    print(f"Student: {result['name']}")
    print(f"Marks: {result['marks']}")
    print(f"Total: {result['total']}")
    print(f"Average: {result['average']:.2f}")
    print(f"Highest: {result['highest']}")
    print(f"Lowest: {result['lowest']}")
    print(f"Passed: {result['passed']}")
    print(f"Failed: {result['failed']}")
    print(f"Grade: {result['grade']}")
    print(f"Result: {result['result']}")
else:
    print("Student not found.")


def show_info(**kwargs):
    print(kwargs)

show_info(name="Ali", age=20, city="Lahore")