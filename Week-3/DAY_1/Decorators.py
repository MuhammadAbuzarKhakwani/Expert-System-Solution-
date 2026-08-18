#Write a decorator called add_exclamation that takes a function returning a string and adds "!" to the end of it.

def add_exclamation(func):
    print(func()+"!")

@add_exclamation
def new_f():
    return "Hello Dawood"

# Write a decorator called validate_types that checks whether
# all arguments passed to a function are integers. If any 
# argument is not an int, it should raise a TypeError with the 
# message "All arguments must be integers" instead of calling 
# the original function.

def decorator_s(my_function):
    Enter = [1,2,"khan"]
    for i in Enter:
        my_function(i)

@decorator_s
def my_function(args):
    if not isinstance(args,int):
        raise TypeError("Zaigham bhai rola aa gaya")
    else:
        print("Theek hai G")





def my_decorator(func):
    print("1. my_decorator is called, wrapping:", func.__name__)
    def wrapper(argss):
        print("3. wrapper is running, before calling original")
        result = func(argss)
        print("5. wrapper is running, after calling original")
        
        return result
        
    wrapper("abuzar,2,a = 1")
    print("2. returning wrapper")
    return wrapper

@my_decorator
def greet(name):
    print("4. greet is actually running with name =", name)
    return f"Hello, {name}"

