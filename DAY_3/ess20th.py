def evod(x):
    if x%2 == 0:
        return 'Even'
    else:
        return 'Odd'

query = int(input("Enter any Number: "))

print(evod(query))


def nameAge(name, age):
    print("Hi, I am", name)
    print("My age is ", age)

print("Case-1:")
nameAge("Dawood", 27)

print("Case-2:")
nameAge(27, "Haris")

