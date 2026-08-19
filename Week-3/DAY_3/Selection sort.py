arr = [10,21,3,4,1,23,82,77]

for i in range(len(arr)):
    min_ = i

    for j in range(i+1,len(arr)):
        if arr[j] < arr[min_]:
            min_ = j
    arr[i], arr[min_] = arr[min_], arr[i]

print(arr)