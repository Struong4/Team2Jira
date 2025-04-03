
#class for an item within the database
#attribute name: the string name of the item
#attribute price: the double price of the item
#attribute quantity: the int quantity of the item
#attribute weight: the double weight of item per one unit

class Item:
    def __init__(self, item_id, name, price, quantity, weight, description, origin, category, quantity_limit):
        self.item_id = str(item_id)  #unique ID
        self.name = name  #item Name
        self.price = float(price)  #price per unit
        self.quantity = int(quantity)  #available Quantity
        self.weight = float(weight)  #weight per unit
        self.description = description  #item Description
        self.origins = origin  #origins
        self.category = category  #categories
        self.quantity_limit = int(quantity_limit)  #quantity limit per user
        
        print(f"Item successfully created!\n"
              f"----------------------------------\n"
              f"Item ID: {self.item_id}\n"
              f"Name: {self.name}\n"
              f"Price (per unit): ${self.price:.2f}\n"
              f"Current Quantity: {self.quantity}\n"
              f"Quantity Limit: {self.quantity_limit}\n"
              f"Weight (per unit): {self.weight} kg\n"
              f"Description: {self.description}\n"
              f"Origins: {self.origins}\n"
              f"Category: {self.category}\n"
              f"----------------------------------\n")


    def __del__(self):
        print(f'Item removed: {self.name} (ID: {self.item_id})\n')

    #accessors
    def getItemID(self):
        return self.item_id

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getQuantity(self):
        return self.quantity

    def getWeight(self):
        return self.weight

    def getDescription(self):
        return self.description

    def getOrigin(self):
        return self.origin

    def getCategory(self):
        return self.category

    def getQuantityLimit(self):
        return self.quantity_limit

    #mutators
    def setItemID(self, new_id):
        self.item_id = str(new_id)

    def setName(self, new_name):
        self.name = new_name

    def setPrice(self, new_price):
        self.price = float(new_price)

    def setQuantity(self, new_quantity):
        self.quantity = int(new_quantity)

    def setWeight(self, new_weight):
        self.weight = float(new_weight)

    def setDescription(self, new_description):
        self.description = new_description

    def setOrigin(self, new_origin):
        self.origin = new_origin if isinstance(new_origin, list) else [new_origin]

    def setCategory(self, new_category):
        self.category = new_category if isinstance(new_category, list) else [new_category]

    def setQuantityLimit(self, new_limit):
        self.quantity_limit = int(new_limit)