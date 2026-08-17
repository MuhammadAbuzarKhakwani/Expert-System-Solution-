class camera:
    def __init__(self, resolution):
        self.resolution = resolution

    def take_photo(self):
        print("Taking a photo using", self.resolution, "mp camera.")


class Gps:
    def __init__(self, location):
        self.location = location

    def show_location(self):
        print("The location at the moment is:", self.location)


class phone:
    def __init__(self, ph_no):
        self.ph_no = ph_no

    def make_call(self,number):
        print("Making a call to", number)


class smartphone(camera, Gps, phone):
    def __init__(self, resolution, location, ph_no):
        camera.__init__(self, resolution)
        Gps.__init__(self, location)
        phone.__init__(self, ph_no)

    def browse_internet(self):
        print("Browsing the internet")

    def display_info(self):
        print("Camera:", self.resolution, "mp")
        print("Location:", self.location)
        print("Phone:", self.ph_no)


s1 = smartphone("108", "Lahore", "03001234567")

s1.take_photo()
s1.show_location()
s1.make_call("03111234567")
s1.browse_internet()
s1.display_info()