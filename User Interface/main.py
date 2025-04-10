from PyQt5 import QtWidgets
from CheckoutScreen import Ui_CheckoutWindow
from LoginPage import Ui_Login
from StudentInventoryView import Ui_StudentInventoryWindow
from StaffInventoryView import Ui_StaffInventoryWindow
from AddInventoryObj import Ui_StaffAddObj
from AddToCart import AddToCartController  # Import the controller we just defined

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
        # Dummy login check
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
        self.ui.GoToCartButton.clicked.connect(self.openCheckoutScreen)
        self.ui.logOutButton.clicked.connect(self.logOut)
        # Create an instance of the add-to-cart controller for this inventory window
        # (Assume "student001" as the current student ID, adjust as needed)
        self.addCartController = AddToCartController(self.ui, "student001", None)
    
    def openCheckoutScreen(self):
        self.checkoutWindow = CheckoutWindow(self)
        # Pass the checkout window reference to the add-to-cart controller so it can update its UI
        self.addCartController.checkoutWindow = self.checkoutWindow
        self.addCartController.updateCheckoutWindow()
        self.checkoutWindow.setGeometry(self.geometry())
        self.checkoutWindow.show()
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

class OpenStaffInventory(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_StaffInventoryWindow()
        self.ui.setupUi(self)
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
        
class CheckoutWindowStaff(QtWidgets.QMainWindow):
    # If needed, create a checkout window for staff
    pass

class OpenAddObjWindow(QtWidgets.QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_StaffAddObj()
        self.ui.setupUi(self)
        self.staffInventory = main_window
        self.ui.cancelButton.clicked.connect(self.goToAddScreen)
        
    def goToAddScreen(self):
        self.staffInventory.setGeometry(self.geometry())
        self.staffInventory.show()
        self.close()
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = LoginScreen()
    window.show()
    sys.exit(app.exec_())