x = int(input("Enter Value of X: "))
y = int(input("Enter Value of Y: "))
z = int(input("Enter Value of Z: "))
n = int(input("Enter Value of N: "))

# data = []

# for i in range(0,x+1):
#     for j in range(0,y+1):
#         for k in range(0,z+1):
#             if i+j+k != n:
#                 data.append([i,j,k])

# print(data)

data = [[i,j,k] for i in range(0,x+1) for j in range(0,y+1) for k in range(0,z+1) if i+j+k != n]
print(data)