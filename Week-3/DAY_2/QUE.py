# enqueue(data)
# dequeue()
# peek()
# is_empty()
# display()

class stack:
    items = []

    def __init__(self):
        self.items = []
    
    def enque(self,data):
        self.items.append(data)
    
    def deque(self):

        if len(self.items) == 0:
            print("Already empty")
        
        else:
            self.items.remove(self.items[0])
    
    def peek(self):
        if len(items) == 0:
            print("Already empty")
        
        else:
            return self.items[0]
    
    def display(self):
        return self.items

    def get_min(self):
        return min(self.items)
    
First = stack()


First.enque(10)
First.enque(20)
First.enque(30)
First.enque(40)
First.enque(50)


print(First.display())

First.deque()

print(First.display())
# print(First.get_min())
