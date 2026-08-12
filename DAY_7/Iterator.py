names = ['Abuzar','khan','khakwani']

my = iter(names)

# print(next(my))


nam = {
    "name": "Muhamad",
    "age": 21
}


nextec = iter(nam)

ne = next(nextec)
# print(nam[ne])

abc = [1,2,3,5]

my = iter(abc)

print(next(my))
print(next(my))


abcd = {
    'a':1,
    'b':2,
    'c':3
}

david = iter(abcd)


print("KEY: ",next(david)," Value: ",abcd[next(david)])


data = ("Python", "C++", "Java", "SQL")

iter_d = iter(data)


i = 0

while i<len(data):
    print(next(iter_d))
    i += 1
