n1 = int(input("Enter a Number: "))
n2 = int(input("Enter another number: "))

print("...........MY program...........")
print("Choose an operation to perform: ")
print("1. Addition")
print("2. Subtraction")
print("3. Multiplication")
print("4. Division")
print("5. Modulus")
print("6. Exponent")
input = int(input("Enter option number: "))

match input:
    case 1:
        print("The Sum of two numbers: ",n1 + n2)
    case 2:
        print("The Difference of two numbers: ",n1 - n2)
    case 3:
        print("The product of two numbers: ",n1*n2)
    case 4:
        print("The Quotient of two numbers: ",n1/n2)
    case 5:
        print("The Remainder of two numbers: ",n1%n2)
    case 6: 
        print("The Exponent of two numbers: ",n1**n2)
    case _:
        print("Invalid Input")
    