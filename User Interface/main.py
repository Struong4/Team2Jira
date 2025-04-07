from PyQt5 import QtCore, QtGui, QtWidgets
from CheckoutScreen import Ui_CheckoutWindow
from StudentInventoryView import Ui_StudentInventoryWindow
from LoginPage import Ui_Login

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
            self.studentInventory.show()
            self.close()
            
        else:
            print("Incorrect Password")
        
    def studentCancelLogin(self):
        self.ui.studentUTextEdit.clear()
        self.ui.studentPTextEdit.clear()
        print("Student Login Canceled")
        
    def staffAcceptLogin(self):
        username = self.ui.staffUTextEdit.toPlainText()
        password = self.ui.staffPTextEdit.toPlainText()
        print(f"Username: {username}, Password: {password}")
        
    def staffCancelLogin(self):
        self.ui.staffUTextEdit.clear()
        self.ui.staffPTextEdit.clear()
        print("Staff Login Canceled")

class OpenStudentInventory(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_StudentInventoryWindow()
        self.ui.setupUi(self)
        # open the checkout window when cart button is clicked
        # will close current window
        self.ui.GoToCartButton.clicked.connect(self.openCheckoutScreen)
    
    def openCheckoutScreen(self):
        self.checkoutWindow = CheckoutWindow(self)
        self.checkoutWindow.show()
        self.hide()
        
class CheckoutWindow(QtWidgets.QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_CheckoutWindow()
        self.ui.setupUi(self)
        self.studentInventory = main_window
        self.ui.goBackButton.clicked.connect(self.goBack)
        
    def goBack(self):
        self.studentInventory.show()
        self.close()
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = LoginScreen()
    window.show()
    sys.exit(app.exec_())