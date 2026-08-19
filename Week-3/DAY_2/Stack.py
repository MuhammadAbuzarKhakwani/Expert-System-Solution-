class stack:
    items = []

    def __init__(self):
        self.items = []
    
    def push(self,data):
        self.items.append(data)
    
    def pop(self):

        if len(self.items) == 0:
            print("Already empty")
        
        else:
            return self.items.pop()
    
    def peek(self):
        if len(items) == 0:
            print("Already empty")
        
        else:
            return self.items[-1]
    
    def display(self):
        return self.items

    def get_min(self):
        return min(self.items)
    
First = stack()

First.pop()

First.push(10)
First.push(20)
First.push(30)
First.push(40)
First.push(50)

First.pop()

print(First.display())

print(First.get_min())
