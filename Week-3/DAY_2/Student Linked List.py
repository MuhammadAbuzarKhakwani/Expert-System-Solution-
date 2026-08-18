class Node:
    def __init__(self,name,roll_no,marks):
        self.name = name 
        self.roll_no = roll_no
        self.marks = marks
        self.next = None
    
class Linked_list:
    def __init__(self):
        self.head = None
    
    def insert_begin(self,name,roll,marks):
        newNode = Node(name,roll,marks)

        newNode.next = self.head
        newNode.prev = self.head
        self.head = newNode

    def insert_middle(self,n1,name,roll,marks):
        newNode = Node(name,roll,marks)

        temp = self.head
        while temp:
            if temp.name == n1:
                newNode.next = temp.next
                temp.next = newNode
            temp = temp.next


    def insert_end(self,name,roll,marks):
        newNode = Node(name,roll,marks)

        if self.head == None:
            self.head = newNode
        
        else:

            temp = self.head

            while temp.next is not None:
                temp = temp.next
            temp.next =  newNode
            newNode.prev = temp
        
    def Search(self):
        key = input("What you want to Search(name,roll): ").lower()

        def search_name(self):
            nam = input("Enter Name to Search: ").lower()

            temp = self.head

            while temp is not None:
                if temp.name == nam:
                    print(f"Roll No:  {temp.roll_no} | Name: {temp.name} | Marks:  {temp.marks}")
                    break
                temp = temp.next
        
        def search_roll(self):
            roll = int(input("Enter Roll Number to Search: "))
            temp = self.head

            while temp is not None:
                if temp.roll_no == roll:
                    print(f"Roll No:  {temp.roll_no} | Name: {temp.name} | Marks:  {temp.marks}")
                    break
                temp = temp.next

        match key:
            case "name":
                search_name(self)

            case "roll":
                search_roll(self)

    def Reverse_List(self):
        prev = None
        temp = self.head

        while temp is not None:
            current = temp.next   
            temp.next = prev     
            prev = temp           
            temp = current       
        self.head = prev          

        

    def Display(self):
        temp = self.head

        while temp is not None:
            print(f"Roll No:  {temp.roll_no} | Name: {temp.name} | Marks:  {temp.marks}")
            temp = temp.next
        
L1 = Linked_list()
L1.insert_begin("ali",101,85)
L1.insert_end("bilal",102,91)
L1.insert_end("dawood",103,78)


L1.insert_middle("bilal","dawood",200,91)
# L1.Search()
# L1.Reverse_List()
L1.Display()






# class Node:
#     def __init__(self,name,roll_no,marks):
#         self.name = name 
#         self.roll_no = roll_no
#         self.marks = marks
#         self.next = None
#         self.prev = None
    
# class Linked_list:
#     def __init__(self):
#         self.head = None
#         self.tail = None
    
#     def insert_begin(self,name,roll,marks):
#         newNode = Node(name,roll,marks)

#         if self.head == None:

#             self.head = newNode
#             self.tail = newNode
#             self.next = None
#             self.prev = None

#         else:
#             newNode.next = self.head #newNode ka next current head ki trf point kar raha hai
#             tail = self.head  #head ko tail keh dia hai humnay
#             self.head = newNode #head update kar diya hai
#             tail.prev = newNode #tail ka previous new Node ki trf point kar raha hai
       


    # def insert_end(self,name,roll,marks):
    #     newNode = Node(name,roll,marks)


        
    #     else:

    #         tail.next = newNode
    #         newNode.prev = tail
    #         tail = newNode
    #         # temp = self.head


    #         # while temp.next is not None:
    #         #     temp = temp.next
    #         # temp.next =  newNode
    #         # newNode.prev = temp
    #         # tail = newNode
        
#     def Search(self):
#         key = input("What you want to Search(name,roll): ").lower()

#         def search_name(self):
#             nam = input("Enter Name to Search: ").lower()

#             temp = self.head

#             while temp is not None:
#                 if temp.name == nam:
#                     print(f"Roll No:  {temp.roll_no} | Name: {temp.name} | Marks:  {temp.marks}")
#                     break
#                 temp = temp.next
        
#         def search_roll(self):
#             roll = int(input("Enter Roll Number to Search: "))
#             temp = self.head

#             while temp is not None:
#                 if temp.roll_no == roll:
#                     print(f"Roll No:  {temp.roll_no} | Name: {temp.name} | Marks:  {temp.marks}")
#                     break
#                 temp = temp.next

#         match key:
#             case "name":
#                 search_name(self)

#             case "roll":
#                 search_roll(self)
          
#     def Display(self):
#         temp = self.head

#         while temp is not None:
#             print(f"Roll No:  {temp.roll_no} | Name: {temp.name} | Marks:  {temp.marks}")
#             temp = temp.next
        

#     def Displa_revers(self):
#         temp = self.tail

#         while temp is not None:
#             print(f"Roll No:  {temp.roll_no} | Name: {temp.name} | Marks:  {temp.marks}")
#             temp = temp.prev
        
# L1 = Linked_list()
# L1.insert_begin("ali",101,85)
# L1.insert_begin("Dawood",102,84)
# L1.insert_begin("Bilal",103,82)

# L1.Displa_revers()
# print("------------------------------------------")
# L1.Display()



