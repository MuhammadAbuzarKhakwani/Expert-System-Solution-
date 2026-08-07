import os 
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_menu():
    print("."*40,"Inventory Managem","."*40)
    print("1.Add product")
    print("2.Update quantity")
    print("3.Remove product")
    print("4.Search product")
    print("5.Display inventory")
    print("6.Exit")

def Add_p(D):
    name = input("Enter Product name: ")
    quantity = int(input("Enter Quantity: "))
    D[name] = quantity

def sl_pause():
    time.sleep(2)




def main():
    D = {}
    print_menu()


main()







