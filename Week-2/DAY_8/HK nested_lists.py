# records = [
#     ["Aliyan", 37.21],
#     ["Khakwani", 37.21],
#     ["Bilal", 37.2],
#     ["Dawood", 41],
#     ["Haris", 39]
# ]

records = []

for _ in range(int(input())):
    name = input()
    score = float(input())

    records.append([name,score])

grades = [rec[1] for rec in records]

grades = list(set(grades))
grades.sort()

second_lowest = grades[1]

names = []
for i in records:
    if i[1] == second_lowest:
        names.append(i[0])

names.sort()

for name in names:
    print(name)

