from crud import addNewItem
from item_class import Item

class Item:
    def __init__(self, id, name, weight, price, quantity, description, origin, category, limit):
        self.id = id
        self.name = name
        self.weight = float(weight)
        self.price = float(price)
        self.quantity = int(quantity)
        self.description = description
        self.origin = origin
        self.category = category
        self.limit = int(limit)

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Weight: {self.weight} lbs, Price: ${self.price}, Quantity: {self.quantity}, Origin: {self.origin}, Category: {self.category}, Limit: {self.limit}"

#reads from example database .txt file
def load_inventory(filename):
    inventory = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            #skip empty lines/headers
            if not line or line.startswith("##"):
                continue
            parts = [p.strip() for p in line.split(',')]
            if len(parts) != 9:
                print(f"Warning: Incorrect format -> {line}")
                continue
            id, name, weight, price, quantity, description, origin, category, limit = parts
            item = Item(id, name, weight, price, quantity, description, origin, category, limit)
            inventory.append(item)
    return inventory

#main shell
def main():
    inventory = load_inventory('C:/Users/benja/Team2Jira/InventoryDatabase/inventory_simulation.txt')
    #iterate through example database and create items in SQL database
    for item in inventory: 
        addNewItem(
            item_id=item.id,
            item_name=item.name,
            weight_lbs=item.weight,
            quantity=item.quantity,
            price=item.price,
            descript=item.description,
            quantity_limit=item.limit,
            origins=[item.origin],
            categories=[item.category]
        )
        print(f"Added {item.name} (ID: {item.id}) to database.")

if __name__ == "__main__":
    main()