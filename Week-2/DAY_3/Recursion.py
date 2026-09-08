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



class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# Create tree
root = Node(1)

root.left = Node(2)
root.right = Node(3)

root.left.left = Node(4)
root.left.right = Node(5)


# Inorder: Left → Root → Right
def inorder(root):
    if root:
        inorder(root.left)
        print(root.value, end=" ")
        inorder(root.right)


# Preorder: Root → Left → Right
def preorder(root):
    if root:
        print(root.value, end=" ")
        preorder(root.left)
        preorder(root.right)


# Postorder: Left → Right → Root
def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.value, end=" ")


# Print results
print("Inorder:")
inorder(root)

print("\nPreorder:")
preorder(root)

print("\nPostorder:")
postorder(root)

