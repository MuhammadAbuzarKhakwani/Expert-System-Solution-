
student = {str(x):{i:x*i for i in range(x)} for x in range(10)}

print(student)

for key,val in student.items():
    print("outer key: ",key)
    for ke,va in val.items():
        print("inner key: ",ke)
        print("value: ",va)
