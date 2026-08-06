data = {} #khali dictionary

data_std = {
    "name" : "Muhammad Abuzar",
    "Roll" : "F2024SE031",
    "Age"  :  21,
    "Nationality" : "Pakistani"
}
print(data)
print(data_std.get("name"))

data_std["city"] = 'lahore'

print(data_std.get("city"))

data_std.pop("Age")

print(data_std)

for ke in data_std:
    print(ke)

for value in data_std.items():
    print(value)

data_std.clear()

print(data_std)

print("....................")
print("....................")


new_std = {
    "name" : "Muhammad Abuzar khakwani",
    "Freind" : "Muhammad Dawood",
}

new_std["Freind"] = "Bilal khan Lodhi"
print(new_std)
new_std["Roll"] = "F2024SE031"
print(new_std)
new_std.pop("Freind")
print(new_std)

for key in new_std:
    print(key)

for k in new_std.values():
    print(k)


students = {
    'Abuzar' : 80,
    'Dawood' : 75,
    'Aliyan' : 85,
    'Bilal'  : 60,
    'Ali'    : 55
}


new_l = list(students.values())

print(new_l)

new_l.sort()


print("The Largest number of Dictionary: ",new_l[-1])






