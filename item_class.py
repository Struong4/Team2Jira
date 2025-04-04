
#class for an item within the database
#attribute name: the string name of the item
#attribute price: the double price of the item
#attribute quantity: the int quantity of the item
#attribute weight: the double weight of item per one unit

class Item:

    #constructor
    def __init__(self, name, price, quantity, weight):
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)
        self.weight = float(weight)
        print(f"New item created: {self.name}\n"
              f"Price (for 1 unit): {self.price}\n"
              f"Current quantity: {self.quantity}\n"
              f"Weight (for 1 unit): {self.weight}\n")    
    #destructor        
    def __del__(self):
        print('Item removed: ' + self.name + '\n')

    #accessor: name
    def getName(self):
        return self.name
    
    #accessor: price
    def getPrice(self):
        return self.price
    
    #accessor: quantity
    def getQuantity(self):
        return self.quantity
    
    #accessor: weight
    def getWeight(self):
        return self.weight
    
    #mutator: name
    def setName(self, newName):
        self.name = newName
        
    #mutator: price
    def setPrice(self, newPrice):
        self.price = newPrice
        
    #mutator: quantity
    def setQuantity(self, newQuantity):
        self.quantity = newQuantity
        
    #mutator: weight
    def setWeight(self, newWeight):
        self.weight = newWeight
        