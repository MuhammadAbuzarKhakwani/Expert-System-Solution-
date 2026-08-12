def count_up_to(n):
    count = 1
    while count < n:
        yield count
        count += 1


for num in count_up_to(11):
    print(num)

def numbers():
    yield 1
    yield 2
    yield 3
    yield 4
    yield 5
    yield 6
    yield 7
    yield 8
    yield 9

get = numbers()

print(next(get))
print(next(get))
print(next(get))
print(next(get))
print(next(get))
print(next(get))
print(next(get))
print(next(get))
print(next(get))





products = [
    {"name": "Laptop", "price": 120000},
    {"name": "Mouse", "price": 2500},
    {"name": "Keyboard", "price": 5000},
    {"name": "Monitor", "price": 35000}
]

def product_gen(prod):
    for pr in prod:
        yield pr

for i in product_gen(products):
    print(i['name']," ",i["price"])