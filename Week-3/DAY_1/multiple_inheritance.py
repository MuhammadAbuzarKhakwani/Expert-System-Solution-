class camera:
    def take_photo(self):
        print("Taking a photo")

class phone:
    def make_call(self):
        print("Making a call")

class smartphone(phone, camera):

    def browse_internet(self):
        print("Browsing the internet")


s1 = smartphone()
s1.make_call()
s1.take_photo()
s1.browse_internet()


class A:
    def show(self):
        print("A")


class B(A):
    def show(self):
        super().show()
        print("B")


class C(A):
    def show(self):
        super().show()
        print("C")


class D(B, C):
    def show(self):
        super().show()
        print("D")


d = D()
d.show()

print(D.__mro__)