arr = [10, 20, 30, 40, 50, 60, 70]

low = 0
high = len(arr) - 1

target = int(input("Enter number to search: "))

while low <= high:

    mid = (low + high) // 2
    
    if arr[mid] == target:
        print(f"Targer found: {arr[mid]}")
        break
    
    elif target < arr[mid]:
        high = mid - 1

    elif target > arr[mid]:
        low = low + 1

else:
    print(f"{target} Not Found")
    