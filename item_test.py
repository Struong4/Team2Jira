import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem)
from item_class import Item  #imports the item class

#constructor: the item manager
#attribute items: an array to store the items of the store
class ItemManager(QWidget):
    def __init__(self):
        super().__init__()
        self.items = []  #array to store Item objects
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout() #vertical box layout

        #INPUT FIELDS
        form_layout = QHBoxLayout() #horizontal box layout
        self.name_input = QLineEdit(self) #input name
        self.price_input = QLineEdit(self) #input price
        self.quantity_input = QLineEdit(self) #input quantity
        self.weight_input = QLineEdit(self) #input weight
        
        #widget formatting
        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Price:"))
        form_layout.addWidget(self.price_input)
        form_layout.addWidget(QLabel("Quantity:"))
        form_layout.addWidget(self.quantity_input)
        form_layout.addWidget(QLabel("Weight:"))
        form_layout.addWidget(self.weight_input)
        
        layout.addLayout(form_layout) #add this layout

        #BUTTONS
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Create Item", self)
        self.remove_button = QPushButton("Remove Item", self)
        self.update_button = QPushButton("Update Quantity", self)
        
        
        #button events
        self.add_button.clicked.connect(self.add_item) #clicked add button
        self.remove_button.clicked.connect(self.remove_item) #clicked remove button
        self.update_button.clicked.connect(self.update_quantity) #clicked update quantity button
        
        button_layout.addWidget(self.add_button) 
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.update_button)
        layout.addLayout(button_layout)

        #TABLE
        self.table = QTableWidget()   
        self.table.setColumnCount(4) #set number of columns
        self.table.setHorizontalHeaderLabels(["Name", "Price (Dollars Per Unit)", "Quantity", "Weight (lbs.)"]) #horizontal headers
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.setWindowTitle("Item Manager") #title
        self.setGeometry(100, 100, 600, 400) 

    #method to add an item
    def add_item(self):
        name = self.name_input.text()
        try:
            price = float(self.price_input.text())
            quantity = int(self.quantity_input.text())
            weight = float(self.weight_input.text())
        except ValueError: #error case: wrong variable type attempted
            print("Invalid input values!")
            return
        
        new_item = Item(name, price, quantity, weight) #use item constructor to create a new Item object
        self.items.append(new_item) #add new item to list of items
        self.update_table() #call table update function

    #method to remove an item
    def remove_item(self):
        selected_row = self.table.currentRow() #set deletion row to currently selected row
        if selected_row >= 0: #valid row input
            del self.items[selected_row] #delete given item
            self.update_table() #call table update function

    #method to update quantity of an item
    def update_quantity(self):
        selected_row = self.table.currentRow() #set updated row to currently selected row
        if selected_row >= 0: #valid row input
            try:
                new_quantity = int(self.quantity_input.text()) #check input in quantity field
                self.items[selected_row].setQuantity(new_quantity) #use Item quantity mutator
                self.update_table() #call table update function
            except ValueError:
                print("Invalid quantity input!") #error case: variable type mismatch
    
    #method to update the table based on user's actions (remove, add, update)
    def update_table(self):
        self.table.setRowCount(len(self.items)) #reset row count
        for row, item in enumerate(self.items):
            self.table.setItem(row, 0, QTableWidgetItem(item.getName()))
            self.table.setItem(row, 1, QTableWidgetItem(str(item.getPrice())))
            self.table.setItem(row, 2, QTableWidgetItem(str(item.getQuantity())))
            self.table.setItem(row, 3, QTableWidgetItem(str(item.getWeight())))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ItemManager()
    window.show()
    sys.exit(app.exec_())
