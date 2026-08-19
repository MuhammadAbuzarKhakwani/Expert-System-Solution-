from collections import defaultdict
from collections import deque
students = defaultdict(list)

students["CS"].append("Ali")
students["CS"].append("Ahmed")

students["SE"].append("Usman")

print(students)

from collections import defaultdict

count = defaultdict(int)

count["apple"] = 99
count["apple"] += 1
count["banana"] += 1

print(count)

student_s = defaultdict(set)

student_s["CS"].add("Ali")
student_s["CS"].add("Ali")

print(student_s)

d = deque([10,15,20])
d.append(11)
d.appendleft(21)

print(d)

print("")

d.pop()
print(d)
d.popleft()
print(d)

d.extend([1000,2000])
print(d)
d.extendleft([100,200])
print(d)
d.rotate(1)
print(d)
d.rotate(-1)
print(d)