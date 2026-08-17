class Bank_account:
    def __init__(self, balance):
        self.__balance = balance
    
    def deposit(self, amount):
        self.__balance += amount

    def display(self):
        print(self.__balance)


abuzar = Bank_account(1500)

abuzar.display()



