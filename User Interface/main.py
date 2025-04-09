from PyQt5 import QtCore, QtGui, QtWidgets
from CheckoutScreen import Ui_CheckoutWindow
from LoginPage import Ui_Login
from StudentInventoryView import Ui_StudentInventoryWindow
from StaffInventoryView import Ui_StaffInventoryWindow
from AddInventoryObj import Ui_StaffAddObj
from item_class import Item

class LoginScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.ui.studentInventory = OpenStudentInventory()
        self.ui.studentButtons.accepted.connect(self.studentAcceptLogin)
        self.ui.studentButtons.rejected.connect(self.studentCancelLogin)
        self.ui.staffButtons.accepted.connect(self.staffAcceptLogin)
        self.ui.staffButtons.rejected.connect(self.staffCancelLogin)
        
    def studentAcceptLogin(self):
        username = self.ui.studentULineEdit.text()
        password = self.ui.studentPLineEdit.text()
        
        # Dummy Login
        if(username == "Group2") and (password == "1234"):
            self.studentInventory = OpenStudentInventory()
            self.studentInventory.setGeometry(self.geometry())
            self.studentInventory.show()
            self.close()
            
        else:
            print("Incorrect Password")
        
    def studentCancelLogin(self):
        self.ui.studentULineEdit.clear()
        self.ui.studentPLineEdit.clear()
        print("Student Login Canceled")
        
    def staffAcceptLogin(self):
        username = self.ui.staffULineEdit.text()
        password = self.ui.staffPLineEdit.text()
        print(f"Username: {username}, Password: {password}")
        
        if(username == "Staff2") and (password == "123123"):
            self.staffInventory = OpenStaffInventory()
            self.staffInventory.setGeometry(self.geometry())
            self.staffInventory.show()
            self.close()
            
        else:
            print("Incorrect Password")
        
    def staffCancelLogin(self):
        self.ui.staffULineEdit.clear()
        self.ui.staffPLineEdit.clear()
        print("Staff Login Canceled")

class OpenStudentInventory(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_StudentInventoryWindow()
        self.ui.setupUi(self)
        # open the checkout window when cart button is clicked
        # will close current window
        self.ui.GoToCartButton.clicked.connect(self.openCheckoutScreen)
        self.ui.logOutButton.clicked.connect(self.logOut)
    
    def openCheckoutScreen(self):
        self.checkoutWindow = CheckoutWindow(self)
        self.checkoutWindow.setGeometry(self.geometry())
        self.checkoutWindow.show()
        self.hide()
        
    def logOut(self):
        self.logInScreen = LoginScreen()
        self.logInScreen.setGeometry(self.geometry())
        self.logInScreen.show()
        self.hide()
        
class OpenStaffInventory(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_StaffInventoryWindow()
        self.ui.setupUi(self)
        # open the checkout window when cart button is clicked
        # will close current window
        self.ui.addObjButton.clicked.connect(self.openNewItemScreen)
        self.ui.logOutButton.clicked.connect(self.logOut)
            
    def openNewItemScreen(self):
        self.addItemWindow = OpenAddObjWindow(self)
        self.addItemWindow.setGeometry(self.geometry())
        self.addItemWindow.show()
        self.hide()
        
    def logOut(self):
        self.logInScreen = LoginScreen()
        self.logInScreen.setGeometry(self.geometry())
        self.logInScreen.show()
        self.hide()
        
class CheckoutWindow(QtWidgets.QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_CheckoutWindow()
        self.ui.setupUi(self)
        self.studentInventory = main_window
        self.ui.goBackButton.clicked.connect(self.goBack)
        
    def goBack(self):
        self.studentInventory.setGeometry(self.geometry())
        self.studentInventory.show()
        self.close()
        
class OpenAddObjWindow(QtWidgets.QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_StaffAddObj()
        self.ui.setupUi(self)
        self.staffInventory = main_window
        self.ui.cancelButton.clicked.connect(self.goToAddScreen)
        self.ui.confirmButton.clicked.connect(self.addObj)
        
    def goToAddScreen(self):
        self.staffInventory.setGeometry(self.geometry())
        self.staffInventory.show()
        self.close()
        
    def addObj(self):       
        # goes back tothe inventory view
        self.saveItemInfo()
        self.staffInventory.setGeometry(self.geometry())
        self.staffInventory.show()
        self.close()
        
    def saveItemInfo(self):
        print("item save triggered")
        
        itemID = self.ui.itemIDText.text().strip()
        name = self.ui.productNameText.text()
        price = self.ui.priceText.text()
        quantity = self.ui.availableQuantitySpinBox.value()
        weight = self.ui.weightText.text()
        description = self.ui.descriptionText.toPlainText()
        quantityLimit = self.ui.limitSpinBox.value()
        
        
        # this uncommented section of code is used to save he image path
        # needs to be connected to sql
        #imageID will be based on 
        """pixmap = self.ui.imageUpload.pixmap()
        buffer = QtCore.QBuffer()
        buffer.open(QtCore.QBuffer.WriteOnly)
        pixmap.save(buffer, "PNG")
        imageData = buffer.data()
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY,
            image BLOB
            )
            ''')

        # Insert or replace image
        cursor.execute('''
        INSERT OR REPLACE INTO images (id, image)
        VALUES (?, ?)
        ''', (imageID, imageData))

        conn.commit()
        conn.close()"""
        
            
        try:
            price = float(price)
        except ValueError:
            print("Price input incorrect format")
            return
            
        try:
            quantity = float(price)
        except ValueError:
            print("Quantity input incorrect format")
            return
            
        try:
            quantityLimit = float(price)
        except ValueError:
            print("Quantity Limit input incorrect format")
            return
            

        origins = []
        categories = []

        #add origins check box
        if self.ui.originCheckBox1.isChecked():
            origins.append(self.ui.originCheckBox1.text())
        if self.ui.originCheckBox2.isChecked():
            origins.append(self.ui.originCheckBox2.text())
        if self.ui.originCheckBox3.isChecked():
            origins.append(self.ui.originCheckBox3.text())
        if self.ui.originCheckBox4.isChecked():
            origins.append(self.ui.originCheckBox4.text()) 

        #add categories check box
        if self.ui.catCheckBox1.isChecked():
            categories.append(self.ui.catCheckBox1.text())
        if self.ui.catCheckBox2.isChecked():
            categories.append(self.ui.catCheckBox2.text())
        if self.ui.catCheckBox3.isChecked():
            categories.append(self.ui.catCheckBox3.text())
        if self.ui.catCheckBox4.isChecked():
            categories.append(self.ui.catCheckBox4.text())
            
        print("=== Product Details ===")
        print(f"Item ID: {itemID}")
        print(f"Name: {name}")
        print(f"Price: {price}")
        print(f"Available Quantity: {quantity}")
        print(f"Weight: {weight}")
        print(f"Description: {description}")
        print(f"Quantity Limit: {quantityLimit}")
        print(f"Origins: {', '.join(origins) if origins else 'None'}")
        print(f"Categories: {', '.join(categories) if categories else 'None'}")
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = LoginScreen()
    window.show()
    sys.exit(app.exec_())