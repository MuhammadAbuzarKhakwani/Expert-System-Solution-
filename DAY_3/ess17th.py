number = [1,2,5,3,2,5,2,11,1]
numbers = [1,2,5,3,2,5,2,11,1]

unique = list(set(number))
unique.sort(reverse = True)
print(unique)

number.extend(numbers)

print(number)

num = number - numbers

print(num)