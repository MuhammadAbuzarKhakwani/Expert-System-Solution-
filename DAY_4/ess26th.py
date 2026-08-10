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
        print(f"Name: {name}, Quantity: {D[name]}")
        # print("Found it")
    else:
        print("This product does not exist")

def Display_p_i(D):
    for key,val in D.items():
        print(f"Product: {key} - Value: {val}") 


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
        
            match choice:
                case 1:
                    clear_screen()
                    Add_p(D)
                case 2:
                    clear_screen()
                    UPD_p(D)
                case 3:
                    clear_screen()
                    del_p(D)
                case 4:
                    clear_screen()
                    search_p(D)
                case 5:
                    clear_screen()
                    Display_p_i(D)
                case 6:
                    clear_screen()
                    c = False
                case _:
                    clear_screen()
                    print("Invalid Input")
        except ValueError:
            print("Banda ban oye!!.Please enter a value from 1-6")
            print("")
    
            
main()




