students = [
    {"name": "Ali", "marks": 78},
    {"name": "Ahmed", "marks": 92},
    {"name": "Sara", "marks": 65},
    {"name": "Hassan", "marks": 85},
    {"name": "Ayesha", "marks": 95}
]

# def get_marks(students):
#     return students["marks"]

get_marks =lambda students: students["marks"]


students.sort(key=get_marks,reverse = True)

print(students)


sum = lambda a,b : print("Sum of: ",a+b)

sum(7,5)

numbers = [10,15,20,30]

sort_list = lambda nums:  nums.sort(reverse = True)

sort_list(numbers)
print(numbers)

products = [
    {"name": "Laptop", "price": 120000},
    {"name": "Mouse", "price": 2500},
    {"name": "Keyboard", "price": 5000},
    {"name": "Monitor", "price": 45000}
]

get_prices = lambda products: products["price"] 

sort_list_dic = lambda products : products.sort(key=get_prices,reverse =True)

sort_list_dic(products)
print(products)



