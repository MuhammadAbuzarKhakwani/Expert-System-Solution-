n1 = int(input("Enter a Number: "))
n2 = int(input("Enter another Number: "))

print("")
print("Choose an operation to perform: ")
print("1. Addition")
print("2. Subtraction")
print("3. Multiplication")
print("4. Division")
inp = int(input("Enter option number: "))

if inp == 1:
    print("The sum of ", n1 , " and ", n2 , " is ", n1 + n2)
elif inp == 2:
    print("The difference of ", n1 , " and ", n2 , " is ", n1 - n2)
elif inp == 3:
    print("The product of ", n1 , " and ", n2 , " is ", n1 * n2)
elif inp == 4:
    print("The quotient of ", n1 , " and ", n2 , " is ", n1 / n2)
else:
    print("Invalid input")

print(type(n1))


del n1
del n2
del inp

