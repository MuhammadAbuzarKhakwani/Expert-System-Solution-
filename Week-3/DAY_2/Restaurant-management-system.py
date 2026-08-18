
class user:
    def __init__(self,name,phone_number,Email):
        self.name = name
        self.Phone_number = phone_number
        self.Email = Email
        

class customer(user):
    customer_id = 1
    def __init__(self,name,phone_number,Email):
        super().__init__(name,phone_number,Email)
        self.customer_id = customer.customer_id
        customer.customer_id += 1
        self.order = []

    def get_food_price(self, food_item):
        prices = {
            "biryani": 500,
            "nihari": 800,
            "karahi": 1200,
            "haleem": 400,
            "seekh kabab": 600,
            "chapli kabab": 350,
            "paya": 700,
            "halwa puri": 250,
            "samosa": 50,
            "gulab jamun": 150
        }
        return prices.get(food_item.lower().strip(), 0)

    def display_menu(self):
        prices = {
            "biryani": 500,
            "nihari": 800,
            "karahi": 1200,
            "haleem": 400,
            "seekh kabab": 600,
            "chapli kabab": 350,
            "paya": 700,
            "halwa puri": 250,
            "samosa": 50,
            "gulab jamun": 150
        }
        for food, price in prices.items():
            print(f"{food.title()}: Rs.{price}")

        print("--------------------------------")
    
    def place_order(self):
        self.display_menu()
        self.Food = input("Enter your Food item here: ")
        self.Quantity = int(input(f"Enter Quantity for : {self.Food}"))

        price = self.get_food_price(self.Food)
        
        if price == 0:
            print("Food Item Not Available")
            return

        self.order.append([self.Food, self.Quantity, price])


    def display(self):
        print(f"Customer id: {self.customer_id}")
        print(f"Customer Name: {self.name}")
        print("...............Your Ordered................ ")

        for item in self.order:
            print(f"Food Item: {item[0]}")
            print(f"Quantity: {item[1]}")
            print(f"Unit Price: {item[2]}")
            print(f"Total: {item[1] * item[2]}")

def main():

    customers = []

    while True:

        print("\n========== FOOD ORDERING SYSTEM ==========")
        print("1. Add Customer")
        print("2. Display Food Menu")
        print("3. Place Order")
        print("4. Display Customer Orders")
        print("5. Exit")

        choice = input("Enter your choice: ")

        match choice:

            case "1":
                name = input("Enter Customer Name: ")
                phone = input("Enter Phone Number: ")
                email = input("Enter Email: ")

                new_customer = customer(name, phone, email)

                customers.append(new_customer)

                print("\nCustomer Added Successfully!")
                print(f"Customer ID: {new_customer.customer_id}")


            case "2":
                if len(customers) == 0:
                    print("Please add a customer first!")

                else:
                    customers[0].display_menu()

            case "3":
                if len(customers) == 0:
                    print("Please add a customer first!")
                    continue

                print("\n------ CUSTOMER LIST ------")

                for person in customers:
                    print(
                        f"ID: {person.customer_id} | "
                        f"Name: {person.name}"
                    )

                customer_id = int(
                    input("\nEnter Customer ID: ")
                )

                found_customer = None

                for person in customers:

                    if person.customer_id == customer_id:
                        found_customer = person
                        break

                if found_customer:
                    found_customer.place_order()
                    print("Order Added Successfully!")

                else:
                    print("Customer Not Found!")

            case "4":
                if len(customers) == 0:
                    print("No customers available!")
                    continue

                print("\n------ CUSTOMER LIST ------")

                for person in customers:
                    print(
                        f"ID: {person.customer_id} | "
                        f"Name: {person.name}"
                    )

                customer_id = int(
                    input("\nEnter Customer ID: ")
                )

                found_customer = None

                for person in customers:

                    if person.customer_id == customer_id:
                        found_customer = person
                        break

                if found_customer:
                    found_customer.display()

                else:
                    print("Customer Not Found!")

            case "5":
                print("Thank you for using the Food Ordering System!")
                break

            case _:
                print("Invalid Choice! Please try again.")


if __name__ == "__main__":
    main()

