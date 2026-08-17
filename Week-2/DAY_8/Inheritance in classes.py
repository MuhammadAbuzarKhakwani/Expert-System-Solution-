# class animal:
#     def __init__(self,name,age):
#         self.name = name 
#         self.age = age 
    
# class dog(animal):
#     def __init__(self,name,age,sound):
#         super().__init__(name,age)
#         self.sound = sound
    

#     def display(self):
#         print(self.name)
#         print(self.age)
#         print(self.sound)


# kutta = dog("poosh",2,"Bhau bhau")

# kutta.display()


# class Animal:
#     def __init__(self,name,age):
#         self.name = name 
#         self.age = age 
    
# class Cat(Animal):
#     def __init__(self,animal,race):
#         super().__init__(animal.name,animal.age)
#         self.race = race

#     def display(self):
#         print(self.name, self.race, self.age)


# A1 = Animal("lusi",2)


# c1 = Cat(A1,"persian")

# c1.display()

class person:
    def __init__(self,name,age,cnic):
        self.name = name 
        self._age = age        #protected ho gaya G
        self.__cnic = cnic     #private ho gaya G
    
    def get_cnic(self):
        return self.__cnic


class student(person):
    def __init__(self,person,dept):
        super().__init__(person.name,person._age,person.get_cnic())
        self.dept = dept
    

    def display(self):
        print(self.name)
        print(self._age)
        print(self.get_cnic())
        print(self.dept)


p1 = person("Abuzar",21,"31303")

st = student(p1,"Software Engineering")

st.display()



    
