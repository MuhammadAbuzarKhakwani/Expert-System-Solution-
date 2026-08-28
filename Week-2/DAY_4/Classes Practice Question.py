class bank:
    def __init__(self, name, pin, balance):
        self.acc_name = name
        self.pin = pin
        self.balance = balance

    def deposit(self, pin, amount):
        if self.pin == pin:
            self.balance += amount
            print("Deposit Successful")
            print("Current Balance:", self.balance)
        else:
            print("Your pin is incorrect! Try again.")

    def withdraw(self, pin, amount):
        if self.pin == pin:
            if self.balance >= amount:
                self.balance -= amount
                print("Withdrawal Successful")
                print("Remaining Balance:", self.balance)
            else:
                print("Insufficient Balance!")
        else:
            print("Incorrect Pin")

    def display_balance(self):
        print(f"Account Holder: {self.acc_name}")
        print(f"Current Balance: {self.balance}")


def display_menu():
    print("---------- Soneri Bank -----------")
    print("---------- Nauman the Great ---------")

    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Display Balance")
    print("5. Exit")
    print("--------------------------------")


def main():
    customers = {}
    count = 0

    while True:
        display_menu()

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Choice!")
            continue

        match choice:

            case 1:
                name = input("Enter your name: ")
                pin = int(input("Set your 4-digit pin: "))
                balance = float(input("Enter initial balance: "))

                count += 1
                customer_id = f"customer{count}"

                customers[customer_id] = bank(name, pin, balance)

                print("\nAccount Created Successfully!")
                print("Your Customer ID is:", customer_id)

            case 2:
                customer_id = input("Enter Customer ID: ")

                if customer_id in customers:
                    pin = int(input("Enter your pin: "))
                    amount = float(input("Enter amount to deposit: "))
                    customers[customer_id].deposit(pin, amount)
                else:
                    print("Customer ID not found")


            case 3:
                customer_id = input("Enter Customer ID: ")

                if customer_id in customers:
                    pin = int(input("Enter your pin: "))
                    amount = float(input("Enter amount to withdraw: "))
                    customers[customer_id].withdraw(pin, amount)
                else:
                    print("Customer ID not found")


            case 4:
                customer_id = input("Enter Customer ID: ")

                if customer_id in customers:
                    pin = int(input("Enter your pin: "))

                    if customers[customer_id].pin == pin:
                        customers[customer_id].display_balance()
                    else:
                        print("Incorrect Pin")
                else:
                    print("Customer ID not found!")



            case 5:
                print("Thank you for using Soneri Bank.")
                break

            case _:
                print("Invalid Choice")


if __name__ == "__main__":
    main()