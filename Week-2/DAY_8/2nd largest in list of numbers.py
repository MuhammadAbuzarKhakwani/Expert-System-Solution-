# n = int(input())
# arr = []

# if 2 <= n <= 10:
#     for i in range(n):
#         data = int(input())
#         arr.append(data)

#     arr = list(set(arr))
#     arr.sort(reverse = True)
#     print(arr[1])

n = int(input())

if 2 <= n <= 10:
    arr = list(map(int ,input().split()[:n]))

for i in arr:
    if -100 >= i >= 100:
        arr.remove(i)

arr = list(set(arr))
arr.sort(reverse = True)
print(arr[1])









