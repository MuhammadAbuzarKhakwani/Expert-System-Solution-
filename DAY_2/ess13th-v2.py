numbers = [] #empty list


for i in range(5):
    num = int(input("Enter any Number: "))
    numbers.append(num)
    

print(numbers)

greatest = numbers[0]
smallest = numbers[0]

i = 1
for i in range(len(numbers)):
    if numbers[i] > numbers[i-1] :
        greatest = numbers[i]

i = 1
for i in range(len(numbers)):
    if numbers[i] < numbers[i-1] :
        smallest = numbers[i]


count_even = 0
odd_count = 0

i = 1
for i in range(len(numbers)):
    if numbers[i]%2 == 0:
        count_even += 1

i = 1
for i in range(len(numbers)):
    if numbers[i]%2 != 0:
        odd_count += 1

print("The Largest value is: ",greatest)
print("The Largest value is: ",smallest)
print("The Even count: ",count_even)
print("The ODD count: ",odd_count)

