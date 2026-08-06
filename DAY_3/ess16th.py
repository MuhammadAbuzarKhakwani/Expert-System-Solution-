
numbers = [i for i in range(11)]

num = [i**2 for i in numbers]


names = ["ali","ahmed","usman"]

new_l = [i.upper() for i in names]
len_l = [len(i) for i in names]
five_l = [i*2 for i in range(5,16)] #Create a list containing numbers from 5 to 15, but store their double values
div_2 = [(i*2)/2 for i in range(5)]
print(numbers)
print("")
print(num)
print("")
print(new_l)
print("")
print(len_l)
print("")
print(five_l)
print("")
print(div_2)

