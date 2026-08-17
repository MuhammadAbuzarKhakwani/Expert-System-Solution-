num = int(input("Enter a Number: "))

if num%2 == 0:
    print("The given number ",num," is Even")
else:
    print("The given number is odd")

print(".................String Operations....................")

name = "Muhammad Abuzar khakwani"

print(name)
print(name.upper())
print(name.lower())
print(len(name))
print(name[0])
print(name[(len(name)-1)])
print(name[::-1])

count = 0

for i in range(len(name)):
    match name[i]:
        case "a":
            count += 1
        case "e":
            count += 1
        case "i":
            count += 1
        case "o":
            count += 1
        case "u":
            count += 1

print("The number of vowels in the given string is ",count)
    




