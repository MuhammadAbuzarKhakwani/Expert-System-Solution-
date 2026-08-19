from collections import OrderedDict


students = OrderedDict()

students["Ali"] = 20
students["Ahmed"] = 21
students["Usman"] = 19
students["Hamza"] = 22

print("Original:")
print(students)

print("Ali's age:")
print(students["Ali"])



print("Is Ahmed present?")

if "Ahmad" in students:
    print("Ahmad is present")

else:
    print("Not present")


students.move_to_end("Ali")

print("After moving Ali to end:")
print(students)


students.move_to_end("Hamza", last=False)

print("\nAfter moving Hamza to beginning:")
print(students)



last_item = students.popitem()

print("Removed last item:")
print(last_item)

print("After removing last:")
print(students)



first_item = students.popitem(last=False)

print("Removed first item:")
print(first_item)

print("After removing first:")
print(students)



students["Bilal"] = 23

print("After adding Bilal:")
print(students)


print("All students:")

for name, age in students.items():
    print(name, age)