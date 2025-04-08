import sys
import sqlite3
from PyQt5 import QtWidgets, QtCore
from StudentInventoryView_1_0 import Ui_MainWindow

class ShoppingCart:
    def __init__(self, student_id):
        """
        Initialize the shopping cart for a specific student.
        """
        self.student_id = student_id
        self.items = {}

    def add_item(self, item_id, quantity=1):
        """
        Add an item to the cart.
        """
        if item_id in self.items:
            self.items[item_id] += quantity
        else:
            self.items[item_id] = quantity
        print(f"Added {quantity} of item '{item_id}' to cart for student '{self.student_id}'.")

    def remove_item(self, item_id, quantity=1):
        """
        Remove a specified quantity of an item from the cart.
        """
        if item_id in self.items:
            self.items[item_id] -= quantity
            if self.items[item_id] <= 0:
                del self.items[item_id]
            print(f"Removed {quantity} of item '{item_id}' from cart for student '{self.student_id}'.")
        else:
            print(f"Item '{item_id}' not found in cart for student '{self.student_id}'.")

    def get_cart_items(self):
        """
        Return the current cart items.
        """
        return self.items

    def checkout(self):
        """
        Process checkout.
        Here you might loop through self.items and use functions from crud.py
        to update the inventory and record the purchase.
        After processing, clear the cart.
        """
        print("Proceeding to checkout with the following items:")
        for item_id, quantity in self.items.items():
            print(f"  Item: {item_id}, Quantity: {quantity}")
        self.items.clear()
        print("Checkout complete. Cart is now empty.")


class StudentInventoryController(QtWidgets.QMainWindow):
    def __init__(self, student_id):
        super().__init__()
        self.student_id = student_id

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.cart = ShoppingCart(student_id)

        self.ui.GoToCartButton.clicked.connect(self.on_checkout_clicked)

        for i in range(1, 17):
            frame = getattr(self.ui, f"objFrame{i}", None)
            if frame:
                frame.installEventFilter(self)

    def eventFilter(self, obj, event):
        """
        When a student clicks on an inventory item frame, add the item to the cart.
        """
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            frame_name = obj.objectName()
            item_id = "item" + frame_name.replace("objFrame", "")
            print(f"{frame_name} clicked. Adding item '{item_id}' to cart.")
            self.cart.add_item(item_id, quantity=1)
            self.update_cart_ui()
            return True
        return super().eventFilter(obj, event)

    def update_cart_ui(self):
        """
        Update the UI (for example, in the status bar) to show current cart contents.
        """
        cart_contents = self.cart.get_cart_items()
        cart_text = "Cart: " + ", ".join([f"{k} ({v})" for k, v in cart_contents.items()])
        self.statusBar().showMessage(cart_text)

    def on_checkout_clicked(self):
        """
        When the "Go To Cart" button is clicked, process the checkout.
        """
        self.cart.checkout()
        self.update_cart_ui()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # test
    student_id = "student001"
    controller = StudentInventoryController(student_id)
    controller.show()

    sys.exit(app.exec_())
