students = [
    {"name": "Ali", "marks": 78},
    {"name": "Ahmed", "marks": 92},
    {"name": "Sara", "marks": 65},
    {"name": "Hassan", "marks": 85},
    {"name": "Ayesha", "marks": 95}
]

def get_marks(students):
    return students["marks"]


students.sort(key=get_marks,reverse = True)

print(students)