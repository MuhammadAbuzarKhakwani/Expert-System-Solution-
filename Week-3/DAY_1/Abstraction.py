from abc import ABC, abstractmethod

class payment(ABC):
    def __init__(self,bal):
        self.bal = bal
    
    @abstractmethod
    def pay(self,amount):
       pass

    @abstractmethod
    def refund(self,amount):
        pass

class creditcard(payment):
    
    def pay(self,amount):
        self.bal -= amount
        print(f"Balance: {self.bal}" )

    def refund(self,amount):
        self.bal += amount
        print(f"Balance: {self.bal}" )

class creditcard(payment):
    
    def pay(self,amount):
        self.bal -= amount
        print(f"Balance: {self.bal}")

    def refund(self,amount):
        self.bal += amount
        print(f"Balance: {self.bal}")

class creditcard(payment):
    
    def pay(self,amount):
        self.bal -= amount
        print(f"Balance: {self.bal}" )

    def refund(self,amount):
        self.bal += amount
        print(f"Balance: {self.bal}" )

class JazzCash(payment):
    
    def pay(self,amount):
        self.bal -= amount
        print(f"Balance: {self.bal}")

    def refund(self,amount):
        self.bal += amount
        print(f"Balance: {self.bal}")

c = creditcard(10000)
j = JazzCash(10000)

c.pay(3000)
c.refund(1000)

j.pay(5000)
j.refund(2000)





    
    


    

