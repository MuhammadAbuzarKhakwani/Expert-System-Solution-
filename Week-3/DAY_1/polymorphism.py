class Dog:
    def sound(self):
        print("Dog barks")


class Cat:
    def sound(self):
        print("Cat meows")


class Cow:
    def sound(self):
        print("Cow moos")


d1 = Dog()
d2 = Cat()
d3 = Cow()

d1.sound()
d2.sound()
d3.sound()
 
# same function name but due to polymorphism behavior changed according to the the objects

