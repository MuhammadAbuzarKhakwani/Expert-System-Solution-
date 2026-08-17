
matrix = [
    [[1,2,3],[4,5,6]],
    [[1,2,3],[4,5,6]],
    [[1,2,3],[4,5,6]]
]

list_f = [[[k*4 for k in i] for i in j] for j in matrix]

list_s = []

for i in matrix:
    for j in i:
        list_s.append(j)



print(list_f)
# print(list_s)