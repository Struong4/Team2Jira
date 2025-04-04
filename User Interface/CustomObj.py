# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CustomObjInCart.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets

import RetrieverEssentials_rc


class CustomObjInCart(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setupUI()
        
    def setupUI(self):
        self.setObjectName("Form")
        self.resize(400, 87)
        
        self.objFrame1_1 = QtWidgets.QFrame(self)
        self.objFrame1_1.setGeometry(QtCore.QRect(9, 9, 222, 69))
        self.objFrame1_1.setFrameShape(QtWidgets.QFrame.Box)
        self.objFrame1_1.setLineWidth(1)
        self.objFrame1_1.setObjectName("objFrame1_1")
        
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.objFrame1_1)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        
        self.label_13 = QtWidgets.QLabel(self.objFrame1_1)
        self.label_13.setMaximumSize(QtCore.QSize(75, 75))
        self.label_13.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        
        self.label_13.setPixmap(QtGui.QPixmap(u":/my_resources/Logos/Upload Image.png"))
        self.label_13.setScaledContents(True)
        self.horizontalLayout_13.addWidget(self.label_13)
        
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        
        self.label_14 = QtWidgets.QLabel(self.objFrame1_1)
        self.label_14.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.label_14.setObjectName("label_14")
        self.verticalLayout_9.addWidget(self.label_14)
        
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        
        self.spinBox_6 = QtWidgets.QSpinBox(self.objFrame1_1)
        self.spinBox_6.setMaximumSize(QtCore.QSize(33, 16777215))
        self.spinBox_6.setObjectName("spinBox_6")
        self.horizontalLayout_14.addWidget(self.spinBox_6)
        
        self.pushButton_7 = QtWidgets.QPushButton(self.objFrame1_1)
        self.pushButton_7.setMinimumSize(QtCore.QSize(46, 0))
        self.pushButton_7.setMaximumSize(QtCore.QSize(75, 16777215))
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_14.addWidget(self.pushButton_7)
        
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem)
        
        self.verticalLayout_9.addLayout(self.horizontalLayout_14)
        
        self.horizontalLayout_13.addLayout(self.verticalLayout_9)
        
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Custom Object in Cart"))
        self.label_13.setText(_translate("Form", "Object Image"))
        self.label_14.setText(_translate("Form", "Object Name - Weight"))
        self.pushButton_7.setText(_translate("Form", "Delete"))
        
    def set_image(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        self.label_13.setPixmap(pixmap.scaled(self.label_13.size(), QtCore.Qt.KeepAspectRatio))
        
    def set_object_name(self, name):
        self.label_14.setText(name)
        
    def set_weight(self,weight):
        self.label_14.setText(f"{self.label_14.text()} - {weight}")
#from customobjincart.py import customObjInCart


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = CustomObjInCart()
    
    #widget.set_image(":/my_resources/Logos/Retriever Essential.png")
    widget.set_object_name("Item Name")
    widget.set_weight("Weight")
    
    widget.show()
    sys.exit(app.exec_())

        
        