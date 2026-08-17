class Bank_account:
    def __init__(self, balance):
        self.__balance = balance
    
    def deposit(self, amount):
        self.__balance += amount
        print("successful Deposit")
        
    def withdraw(self,amount):
        if self.__balance < amount:
            print("Insufficient balance")
        else:
            print("Balnce before transaction: ",self.__balance)
            self.__balance -= amount
            print("successful transaction")
            print("Balnce after transaction: ",self.__balance)

    def display(self):
        print(self.__balance)



data = int(input("Enter your balance: "))


abuzar = Bank_account(data)

abuzar.display()
abuzar.deposit(500)
abuzar.withdraw(3000)
abuzar.withdraw(300)


class student:
    
    def __init__(self, number):
        self.__marks = number

    @property
    def mark(self):
        return self.__marks
    
    @mark.setter
    def mark(self,val):
        if val < 100:
            self.__marks = val
        else:
            print("Invalid marks")


s1 = student(122)


s1.mark = 53

a = s1.mark



print(a)

