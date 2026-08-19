# Your program must:

# Create a Counter from the list.
# Display the frequency of each number.
# Find the 3 most frequently occurring numbers using most_common().

from collections import Counter

numbers = [
    4, 2, 7, 4, 2, 9, 4,
    7, 7, 3, 2, 9, 4, 7
]

# task no 1
a = Counter(numbers)

for k,v in a.items():
    print(f"Number: {k}  count: {v}")

print("")
print("")

# task no 2

d = a.most_common(3)

for i in d:
    print(f"Number: {i[0]} has occured : {i[1]}")


# task no 3
print("")
print(f"Total Elements: {a.total()}")


