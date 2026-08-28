talib_e_ilm = [
    {"name": "Ali", "age": 22},
    {"name": "Ahmed", "age": 19},
    {"name": "Sara", "age": 21},
    {"name": "Hassan", "age": 18}
]

get_age = lambda talib : talib["age"]

sort_by_age = lambda talib : talib.sort(key=get_age)

for i in talib_e_ilm:
    print(i["name"],": ",i["age"])
