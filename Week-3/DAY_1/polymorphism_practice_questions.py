class Employee:
    def __init__(self, name, ph_no):
        self.__name = name
        self.__ph_no = ph_no

    @property
    def data(self):
        return self.__name, self.__ph_no


class Full_time(Employee):
    def __init__(self, name, data, stack):
        super().__init__(name, data)
        self.stack = stack

    def contact_salary(self):
        print("Full-Time Salary: 1 Lac Rupees")


class Part_time(Employee):
    def __init__(self, name, data, social_ap):
        super().__init__(name, data)
        self.social_ap = social_ap

    def contact_salary(self):
        print("Part-Time Salary: 25,000 Rupees")


class Remote(Employee):
    def __init__(self, name, data, level):
        super().__init__(name, data)
        self.level = level

    def contact_salary(self):
        print("Remote: 150,000 Rupees")


E1 = Full_time("Abuzar", "0301-7650966", "Python-Django")
E2 = Part_time("Dawood", "0301-7650966", "Slack")
E3 = Remote("Nouman", "0301-7650966", "Senior")


E1.contact_salary()
E2.contact_salary()
E3.contact_salary()