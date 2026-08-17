class PDF:
    def read(self):
        print("Reading PDF document")


class WordDocument:
    def read(self):
        print ("Reading Word document")


class Image:
    def display(self):
        print ("Displaying image")

    


def duck_t(obj):
    obj.read()


p = PDF()
w = WordDocument()
i = Image()


duck_t(p)
duck_t(w)
i.display()

