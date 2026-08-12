def fact_l(n):
    if n == 0:
        return 1
    else:
        return n*fact_l(n-1)

s = int(input("Enter a Number: "))
number = fact_l(s)

print(number)

n = int(input("Enter a Number: "))

def fun_print(n):
    if n!=0:
        fun_print(n-1)
        print(n)
    else:
        print("\nFinished")
fun_print(n)

def print_pyra(n):
    if n <= 0:
        print("Enter +ve number please!: ")
    else:
        print_pyra(n-1)
        print("*"*n)

print_pyra(n)
def print_pyras(n):
    if n <= 0:
        print("Enter +ve number please!: ")
    else:
        print("*"*n)
        print_pyras(n-1)

print_pyras(n)

