list_a =[1,2,2,2,3,3,3,4,4,4,4,4,3,3,3,3]


list_a = set(list_a)
list_a = list(list_a)
list_a.sort()

dic_l = {}

for i in list_a:
    if i in dic_l:
        dic_l[i] += 1
    else:
        dic_l[i] = 1

print(dic_l)

print(list_a[-2])

#invert dictionary



student = {
    'name' : "abuzar",
    'age' : 21
}

std = {}

for key,val in student.items():
    std[val] = key

print(std)


student["name"] = "khakwani"

for key in student:
    print(key)

for i in student.values():
    print(i)
    
for k,w in student.items():
    print(k," ",w)

student["surname"] = "khakwani"