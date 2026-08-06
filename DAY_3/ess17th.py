number = [1,2,5,3,2,5,2,11,1]
numbers = [1,2,5,3,2,5,2,11,1]

unique = list(set(number))
unique.sort(reverse = True)





nested_l = [[j for j in numbers] for i in range(5)]

nested_table = [i*j for i in range(1,11) for j in range(2,3)]

print(nested_table)

nums = int(input("Enter any Number for Table: "))
table = [nums*i for i in range(1,11)]

print(table)
