from PyQt5 import QtWidgets, QtCore
from datetime import datetime
from InventoryDatabase import crud
from UserInterface.CustomObj import CustomObjInCart

# ---------------------------------------
# In-Memory Shopping Cart with Debugging
# ---------------------------------------
class ShoppingCart:
    def __init__(self, student_id):
        self.student_id = student_id
        self.items = {}
        print(f"[DEBUG] ShoppingCart created for student '{student_id}'.")

    def add_item(self, item_id, quantity=1):
        print(f"[DEBUG] Attempting to add {quantity} of '{item_id}' to cart.")
        if item_id in self.items:
            self.items[item_id] += quantity
        else:
            self.items[item_id] = quantity
        print(f"[DEBUG] Cart contents after adding: {self.items}")

    def remove_item(self, item_id, quantity=1):
        print(f"[DEBUG] Attempting to remove {quantity} of '{item_id}' from cart.")
        if item_id in self.items:
            self.items[item_id] -= quantity
            if self.items[item_id] <= 0:
                del self.items[item_id]
            print(f"[DEBUG] Cart contents after removal: {self.items}")
        else:
            print(f"[DEBUG] Item '{item_id}' not found in cart.")

    def get_cart_items(self):
        return self.items

    def checkout(self):
        print("[DEBUG] Starting checkout process...")
        for item_id, quantity in self.items.items():
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[DEBUG] Processing item '{item_id}' (Quantity: {quantity}) at {now_str}")
            result = crud.buyItem(self.student_id, item_id, now_str, quantity)
            if "✅" in result:
                print(f"[DEBUG] Processed purchase for '{item_id}' (qty: {quantity}).")
            else:
                print(f"[DEBUG] Failed to process purchase for '{item_id}': {result}")
        self.items.clear()
        print("[DEBUG] Checkout complete. Cart is now empty.")


# --------------------------------------------------------------
# Controller: Integrate Add-to-Cart functionality into Inventory UI
# --------------------------------------------------------------
class AddToCartController(QtCore.QObject):
    def __init__(self, inventoryUI, student_id, checkoutWindow=None):
        """
        :param inventoryUI: The UI instance from your StudentInventoryView.
        :param student_id: The current student's ID.
        :param checkoutWindow: Optional CheckoutWindow instance to update its display.
        """
        super().__init__()
        self.inventoryUI = inventoryUI
        self.student_id = student_id
        self.checkoutWindow = checkoutWindow
        self.cart = ShoppingCart(student_id)
        print(f"[DEBUG] AddToCartController initialized for student '{student_id}'.")

        # Find the parent container where you add the item widgets.
        if hasattr(self.inventoryUI, "scrollAreaWidgetContents"):
            parent = self.inventoryUI.scrollAreaWidgetContents
            print("[DEBUG] Using inventoryUI.scrollAreaWidgetContents as parent for item search.")
        else:
            parent = self.inventoryUI
            print("[DEBUG] scrollAreaWidgetContents not found, using inventoryUI itself.")

        if parent is None:
            print("[DEBUG] Error: Parent container is None. Cannot search for child widgets.")
        else:
        # Instead of searching specifically for QFrame, pass None for the class type 
        # so we find *all* widgets named objFrame*. This includes custom classes 
        # that do not inherit from QFrame.
            item_widgets = parent.findChildren(QtWidgets.QWidget, QtCore.QRegExp("^objFrame.*"))
            print(f"[DEBUG] Found {len(item_widgets)} inventory item widgets matching 'objFrame.*'.")

            for widget in item_widgets:
                print(f"[DEBUG] Installing event filter on widget '{widget.objectName()}'.")
                widget.setAttribute(QtCore.Qt.WA_Hover, True)
                widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        print(f"[DEBUG] eventFilter: Object '{obj.objectName()}' received event type {event.type()}.")
        if event.type() == QtCore.QEvent.Enter:
            print(f"[DEBUG] Mouse entered '{obj.objectName()}'.")
            obj.setStyleSheet("background-color: rgba(0, 120, 215, 50);")
            return False

        elif event.type() == QtCore.QEvent.Leave:
            print(f"[DEBUG] Mouse left '{obj.objectName()}'.")
            obj.setStyleSheet("")
            return False

        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            print(f"[DEBUG] MouseButtonRelease on '{obj.objectName()}'.")
            frame_name = obj.objectName()
            item_id = "item" + frame_name.replace("objFrame", "")
            print(f"[DEBUG] Adding item '{item_id}' to cart.")
            self.cart.add_item(item_id, 1)
            self.updateCheckoutWindow()
            return True
        return super().eventFilter(obj, event)

    def updateCheckoutWindow(self):
        """
        Updates the CheckoutScreen UI with current cart items.
        """
        if not self.checkoutWindow:
            print("[DEBUG] No checkout window available; skipping UI update.")
            return
        
        layout = self.checkoutWindow.ui.verticalLayout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for item_id, quantity in self.cart.get_cart_items().items():
            image_path = ":/my_resources/Logos/Retriever Essential.png"
            display_name = item_id
            display_info = f"Qty: {quantity}"
            print(f"[DEBUG] Updating checkout UI: Adding '{item_id}' with {display_info}.")
            cart_item = CustomObjInCart()
            cart_item.set_image(image_path)
            cart_item.set_object_name(display_name)
            cart_item.set_weight(display_info)
            layout.addWidget(cart_item)

        if hasattr(self.checkoutWindow.ui, "label_8"):
            total = sum(self.cart.get_cart_items().values())
            self.checkoutWindow.ui.label_8.setText(str(total))
            print(f"[DEBUG] Total items updated to {total} in checkout UI.")
