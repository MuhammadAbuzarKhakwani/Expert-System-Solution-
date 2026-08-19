from collections import defaultdict

students = defaultdict(list)

students["CS"].append("Ali")
students["CS"].append("Ahmed")

students["SE"].append("Usman")

print(students)