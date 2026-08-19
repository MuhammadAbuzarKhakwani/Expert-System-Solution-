from collections import Counter

numbers = [1,1,1,4,4]


count = Counter(numbers)

print(count.most_common())
print(count.get(1))

result = Counter(numbers)

print(result)

text = "Muhammad Abuzar Khakwani"

count = Counter(text)

print(count.most_common())


c = {
    'apple': 3,
    'banana': 2,
    'orange': 5
}

g = Counter(c)
print(g)
print(g.most_common(1))
print(g.get('apple'))

d = Counter("mississippi")
d.update("apple")
print(d['s'])
print(d['i'])
print(d['p'])
print(d['x'])

d.update("apple")
print(Counter(d))

total = g+d
print(total)

total = g-d
print(total)

print(list(d.elements()))