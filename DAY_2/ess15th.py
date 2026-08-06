numbers = (1,2,4,2,1)

print(len(numbers))

print("1st",numbers[0])
print("2nd",numbers[1])
print("3rd",numbers[2])
print("4th",numbers[3])
print("5th",numbers[4])


print(numbers.count(2))
print(numbers.index(2))

student = ("david",21,'computer')

name,age,subject = student


print(name)
print(age)
print(subject)

student = ("Ali", 21, ("CS", "Python"))

name, age, (department, language) = student

print(name)
print(age)
print(department)
print(language)