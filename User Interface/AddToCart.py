from PyQt5 import QtWidgets, QtCore
from datetime import datetime
import crud
from CustomObj import CustomObjInCart

class ShoppingCart:
    def __init__(self, student_id):
        self.student_id = student_id
        self.items = {}

    def add_item(self, item_id, quantity=1):
        if item_id in self.items:
            self.items[item_id] += quantity
        else:
            self.items[item_id] = quantity

    def remove_item(self, item_id, quantity=1):
        if item_id in self.items:
            self.items[item_id] -= quantity
            if self.items[item_id] <= 0:
                del self.items[item_id]

    def get_cart_items(self):
        return self.items

    def checkout(self):
        for item_id, quantity in self.items.items():
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = crud.buyItem(self.student_id, item_id, now_str, quantity)
        self.items.clear()

class AddToCartController(QtCore.QObject):
    def __init__(self, inventoryUI, student_id, checkoutWindow=None):
        super().__init__()
        self.inventoryUI = inventoryUI
        self.student_id = student_id
        self.checkoutWindow = checkoutWindow
        self.cart = ShoppingCart(student_id)

        if hasattr(self.inventoryUI, "scrollAreaWidgetContents"):
            parent = self.inventoryUI.scrollAreaWidgetContents
        else:
            parent = self.inventoryUI

        if parent is not None:
            item_widgets = parent.findChildren(QtWidgets.QWidget, QtCore.QRegExp("^objFrame.*"))
            for widget in item_widgets:
                widget.setAttribute(QtCore.Qt.WA_Hover, True)
                widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Enter:
            obj.setStyleSheet("background-color: rgba(0, 120, 215, 50);")
            return False

        elif event.type() == QtCore.QEvent.Leave:
            obj.setStyleSheet("")
            return False

        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            frame_name = obj.objectName()
            item_id = "item" + frame_name.replace("objFrame", "")
            self.cart.add_item(item_id, 1)
            self.updateCheckoutWindow()
            return True
        return super().eventFilter(obj, event)

    def updateCheckoutWindow(self):
        if not self.checkoutWindow:
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
            cart_item = CustomObjInCart()
            cart_item.set_image(image_path)
            cart_item.set_object_name(display_name)
            cart_item.set_weight(display_info)
            layout.addWidget(cart_item)

        if hasattr(self.checkoutWindow.ui, "label_8"):
            total = sum(self.cart.get_cart_items().values())
            self.checkoutWindow.ui.label_8.setText(str(total))
