class Node:
    def __init__(self,data):
        self.data = data
        self.next = None
    
class LL:
    def __init__(self):
        self.head = None
    def Insert_end(self,data):
        newNode = Node(data)
        
        temp = self.head

        while temp.next is not None:
            temp = temp.next 
        
        temp.next = newNode

    def Inser_beginning(self,data):
        newNode = Node(data)

        newNode.next = self.head
        self.head = newNode
    
    def display(self):
        temp = self.head

        while temp is not None:
            print(temp.data, end=" -> ")
            temp = temp.next

new = LL()

new.Inser_beginning(1)
new.Inser_beginning(2)
new.Inser_beginning(3)
new.Inser_beginning(4)

new.Insert_end("khan")


new.display()