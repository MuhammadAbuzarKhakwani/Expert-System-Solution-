
matrix = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]

list_f = [j for i in matrix for j in i]
'''
for i in matrix:
    for j in i:
        list_f.append(j)'''



print(list_f)