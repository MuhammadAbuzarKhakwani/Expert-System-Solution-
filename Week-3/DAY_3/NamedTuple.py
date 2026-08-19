# student = ("Ali", 20, "CS")

# print(student[0])
# print(student[1])
# print(student[2])

from collections import namedtuple

Student = namedtuple("student",["name","age","department"])

student = Student("Ali", 20, "CS")

print(student.name)
print(student.age)
print(student.department)

Employee = namedtuple("employee",["name","salary"])

employee = Employee("Abuzar Khan",20000)

print(employee.name)
print(employee.salary)



