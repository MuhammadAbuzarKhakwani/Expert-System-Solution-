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

def UPD_p(D):
    Add_p(D)

def del_p(D):
    name = input("Enter Product name to Delete: ")
    if name in D:
        del D[name]
    else:
        print("This product does not exist")

def search_p(D):
    name = input("Enter product to Search: ")
    if name in D:
        print("Found it")

def Display_p_i(D):
    for key in D:
        print("Products: ",key) 


def sl_pause():
    time.sleep(1.5)




def main():
    D = {}
    c = True
    while c:
        sl_pause()
        clear_screen()

        print_menu()
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Banda ban oye!!.Please enter a value from 1-6")
            print("")

        match choice:
            case 1:
                Add_p(D)
            case 2:
                UPD_p(D)
            case 3:
                del_p(D)
            case 4:
                search_p(D)
            case 5:
                Display_p_i(D)
            case 6:
                c = False
            case _:
                print("Invalid Input")
        
            
main()




