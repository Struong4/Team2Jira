# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StudentInventoryView.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(False)
        Dialog.resize(677, 493)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setObjectName("frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(10, -1, 10, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_106 = QtWidgets.QLabel(self.frame)
        self.label_106.setMinimumSize(QtCore.QSize(0, 75))
        self.label_106.setObjectName("label_106")
        self.verticalLayout_2.addWidget(self.label_106)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalSlider = QtWidgets.QSlider(self.frame)
        self.horizontalSlider.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout_2.addWidget(self.horizontalSlider)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setEnabled(False)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.checkBox = QtWidgets.QCheckBox(self.frame)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_2.addWidget(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.frame)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout_2.addWidget(self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(self.frame)
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout_2.addWidget(self.checkBox_3)
        self.checkBox_4 = QtWidgets.QCheckBox(self.frame)
        self.checkBox_4.setObjectName("checkBox_4")
        self.verticalLayout_2.addWidget(self.checkBox_4)
        spacerItem = QtWidgets.QSpacerItem(20, 128, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(20, 178, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 308, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.SearchBar = QtWidgets.QLineEdit(self.frame)
        self.SearchBar.setText("")
        self.SearchBar.setObjectName("SearchBar")
        self.horizontalLayout_3.addWidget(self.SearchBar)
        self.horizontalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.SortByLabel = QtWidgets.QLabel(self.frame)
        self.SortByLabel.setObjectName("SortByLabel")
        self.horizontalLayout_2.addWidget(self.SortByLabel)
        self.SortByComboBox = QtWidgets.QComboBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SortByComboBox.sizePolicy().hasHeightForWidth())
        self.SortByComboBox.setSizePolicy(sizePolicy)
        self.SortByComboBox.setMinimumSize(QtCore.QSize(100, 0))
        self.SortByComboBox.setObjectName("SortByComboBox")
        self.SortByComboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.SortByComboBox)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.GoToCartButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GoToCartButton.sizePolicy().hasHeightForWidth())
        self.GoToCartButton.setSizePolicy(sizePolicy)
        self.GoToCartButton.setMinimumSize(QtCore.QSize(75, 23))
        self.GoToCartButton.setMaximumSize(QtCore.QSize(100, 23))
        self.GoToCartButton.setObjectName("GoToCartButton")
        self.horizontalLayout.addWidget(self.GoToCartButton)
        self.verticalLayout_7.addLayout(self.horizontalLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_17.addWidget(self.label_6, 0, QtCore.Qt.AlignHCenter)
        self.graphicsView_15 = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_15.setObjectName("graphicsView_15")
        self.verticalLayout_17.addWidget(self.graphicsView_15)
        self.gridLayout_2.addLayout(self.verticalLayout_17, 0, 0, 1, 1)
        self.verticalLayout_22 = QtWidgets.QVBoxLayout()
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.label_21 = QtWidgets.QLabel(self.frame)
        self.label_21.setObjectName("label_21")
        self.verticalLayout_22.addWidget(self.label_21, 0, QtCore.Qt.AlignHCenter)
        self.graphicsView_20 = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_20.setObjectName("graphicsView_20")
        self.verticalLayout_22.addWidget(self.graphicsView_20)
        self.gridLayout_2.addLayout(self.verticalLayout_22, 2, 0, 1, 1)
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.label_17 = QtWidgets.QLabel(self.frame)
        self.label_17.setObjectName("label_17")
        self.verticalLayout_18.addWidget(self.label_17, 0, QtCore.Qt.AlignHCenter)
        self.graphicsView_16 = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_16.setObjectName("graphicsView_16")
        self.verticalLayout_18.addWidget(self.graphicsView_16)
        self.gridLayout_2.addLayout(self.verticalLayout_18, 1, 0, 1, 1)
        self.verticalLayout_90 = QtWidgets.QVBoxLayout()
        self.verticalLayout_90.setObjectName("verticalLayout_90")
        self.label_89 = QtWidgets.QLabel(self.frame)
        self.label_89.setObjectName("label_89")
        self.verticalLayout_90.addWidget(self.label_89, 0, QtCore.Qt.AlignHCenter)
        self.graphicsView_88 = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_88.setObjectName("graphicsView_88")
        self.verticalLayout_90.addWidget(self.graphicsView_88)
        self.gridLayout_2.addLayout(self.verticalLayout_90, 3, 1, 1, 1)
        self.verticalLayout_23 = QtWidgets.QVBoxLayout()
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.label_22 = QtWidgets.QLabel(self.frame)
        self.label_22.setObjectName("label_22")
        self.verticalLayout_23.addWidget(self.label_22, 0, QtCore.Qt.AlignHCenter)
        self.graphicsView_21 = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_21.setObjectName("graphicsView_21")
        self.verticalLayout_23.addWidget(self.graphicsView_21)
        self.gridLayout_2.addLayout(self.verticalLayout_23, 1, 2, 1, 1)
        self.verticalLayout_19 = QtWidgets.QVBoxLayout()
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.label_18 = QtWidgets.QLabel(self.frame)
        self.label_18.setObjectName("label_18")
        self.verticalLayout_19.addWidget(self.label_18, 0, QtCore.Qt.AlignHCenter)
        self.graphicsView_17 = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_17.setObjectName("graphicsView_17")
        self.verticalLayout_19.addWidget(self.graphicsView_17)
        self.gridLayout_2.addLayout(self.verticalLayout_19, 0, 1, 1, 1)
        self.verticalLayout_21 = QtWidgets.QVBoxLayout()
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.label_20 = QtWidgets.QLabel(self.frame)
        self.label_20.setObjectName("label_20")
        self.verticalLayout_21.addWidget(self.label_20, 0, QtCore.Qt.AlignHCenter)
        self.graphicsView_19 = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_19.setObjectName("graphicsView_19")
        self.verticalLayout_21.addWidget(self.graphicsView_19)
        self.gridLayout_2.addLayout(self.verticalLayout_21, 1, 1, 1, 1)
        self.verticalLayout_63 = QtWidgets.QVBoxLayout()
        self.verticalLayout_63.setObjectName("verticalLayout_63")
        self.label_62 = QtWidgets.QLabel(self.frame)
        self.label_62.setObjectName("label_62")
        self.verticalLayout_63.addWidget(self.label_62, 0, QtCore.Qt.AlignHCenter)
        self.graphicsView_61 = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_61.setObjectName("graphicsView_61")
        self.verticalLayout_63.addWidget(self.graphicsView_61)
        self.gridLayout_2.addLayout(self.verticalLayout_63, 3, 0, 1, 1)
        self.verticalLayout_36 = QtWidgets.QVBoxLayout()
        self.verticalLayout_36.setObjectName("verticalLayout_36")
        self.label_35 = QtWidgets.QLabel(self.frame)
        self.label_35.setObjectName("label_35")
        self.verticalLayout_36.addWidget(self.label_35, 0, QtCore.Qt.AlignHCenter)
        self.graphicsView_34 = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_34.setObjectName("graphicsView_34")
        self.verticalLayout_36.addWidget(self.graphicsView_34)
        self.gridLayout_2.addLayout(self.verticalLayout_36, 0, 2, 1, 1)
        self.verticalLayout_27 = QtWidgets.QVBoxLayout()
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.label_26 = QtWidgets.QLabel(self.frame)
        self.label_26.setObjectName("label_26")
        self.verticalLayout_27.addWidget(self.label_26, 0, QtCore.Qt.AlignHCenter)
        self.graphicsView_25 = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_25.setObjectName("graphicsView_25")
        self.verticalLayout_27.addWidget(self.graphicsView_25)
        self.gridLayout_2.addLayout(self.verticalLayout_27, 2, 3, 1, 1)
        self.verticalLayout_26 = QtWidgets.QVBoxLayout()
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.label_25 = QtWidgets.QLabel(self.frame)
        self.label_25.setObjectName("label_25")
        self.verticalLayout_26.addWidget(self.label_25, 0, QtCore.Qt.AlignHCenter)
        self.graphicsView_24 = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_24.setObjectName("graphicsView_24")
        self.verticalLayout_26.addWidget(self.graphicsView_24)
        self.gridLayout_2.addLayout(self.verticalLayout_26, 1, 3, 1, 1)
        self.verticalLayout_20 = QtWidgets.QVBoxLayout()
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.label_19 = QtWidgets.QLabel(self.frame)
        self.label_19.setObjectName("label_19")
        self.verticalLayout_20.addWidget(self.label_19, 0, QtCore.Qt.AlignHCenter)
        self.graphicsView_18 = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_18.setObjectName("graphicsView_18")
        self.verticalLayout_20.addWidget(self.graphicsView_18)
        self.gridLayout_2.addLayout(self.verticalLayout_20, 2, 1, 1, 1)
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_16 = QtWidgets.QLabel(self.frame)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_16.addWidget(self.label_16, 0, QtCore.Qt.AlignHCenter)
        self.graphicsView_14 = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_14.setObjectName("graphicsView_14")
        self.verticalLayout_16.addWidget(self.graphicsView_14)
        self.gridLayout_2.addLayout(self.verticalLayout_16, 2, 2, 1, 1)
        self.verticalLayout_48 = QtWidgets.QVBoxLayout()
        self.verticalLayout_48.setObjectName("verticalLayout_48")
        self.label_47 = QtWidgets.QLabel(self.frame)
        self.label_47.setObjectName("label_47")
        self.verticalLayout_48.addWidget(self.label_47, 0, QtCore.Qt.AlignHCenter)
        self.graphicsView_46 = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_46.setObjectName("graphicsView_46")
        self.verticalLayout_48.addWidget(self.graphicsView_46)
        self.gridLayout_2.addLayout(self.verticalLayout_48, 0, 3, 1, 1)
        self.verticalLayout_105 = QtWidgets.QVBoxLayout()
        self.verticalLayout_105.setObjectName("verticalLayout_105")
        self.label_104 = QtWidgets.QLabel(self.frame)
        self.label_104.setObjectName("label_104")
        self.verticalLayout_105.addWidget(self.label_104, 0, QtCore.Qt.AlignHCenter)
        self.graphicsView_103 = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_103.setObjectName("graphicsView_103")
        self.verticalLayout_105.addWidget(self.graphicsView_103)
        self.gridLayout_2.addLayout(self.verticalLayout_105, 3, 2, 1, 1)
        self.verticalLayout_106 = QtWidgets.QVBoxLayout()
        self.verticalLayout_106.setObjectName("verticalLayout_106")
        self.label_105 = QtWidgets.QLabel(self.frame)
        self.label_105.setObjectName("label_105")
        self.verticalLayout_106.addWidget(self.label_105, 0, QtCore.Qt.AlignHCenter)
        self.graphicsView_104 = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_104.setObjectName("graphicsView_104")
        self.verticalLayout_106.addWidget(self.graphicsView_104)
        self.gridLayout_2.addLayout(self.verticalLayout_106, 3, 3, 1, 1)
        self.verticalLayout_7.addLayout(self.gridLayout_2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_7)
        self.horizontalLayout_5.addWidget(self.frame)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_106.setText(_translate("Dialog", "UMBC Logo"))
        self.label_2.setText(_translate("Dialog", "Slider Label"))
        self.label.setText(_translate("Dialog", "Catagories"))
        self.checkBox.setText(_translate("Dialog", "Cat1"))
        self.checkBox_2.setText(_translate("Dialog", "Cat2"))
        self.checkBox_3.setText(_translate("Dialog", "Cat3"))
        self.checkBox_4.setText(_translate("Dialog", "Cat4"))
        self.SortByLabel.setText(_translate("Dialog", "Sort By:"))
        self.SortByComboBox.setItemText(0, _translate("Dialog", "Name"))
        self.pushButton.setText(_translate("Dialog", "<"))
        self.pushButton_2.setText(_translate("Dialog", ">"))
        self.GoToCartButton.setText(_translate("Dialog", "GoToCart"))
        self.label_6.setText(_translate("Dialog", "Obj1 Title"))
        self.label_21.setText(_translate("Dialog", "Obj4 Title"))
        self.label_17.setText(_translate("Dialog", "Obj1 Title"))
        self.label_89.setText(_translate("Dialog", "Obj4 Title"))
        self.label_22.setText(_translate("Dialog", "Obj1 Title"))
        self.label_18.setText(_translate("Dialog", "Obj1 Title"))
        self.label_20.setText(_translate("Dialog", "Obj1 Title"))
        self.label_62.setText(_translate("Dialog", "Obj4 Title"))
        self.label_35.setText(_translate("Dialog", "Obj1 Title"))
        self.label_26.setText(_translate("Dialog", "Obj3 Title"))
        self.label_25.setText(_translate("Dialog", "Obj3 Title"))
        self.label_19.setText(_translate("Dialog", "Obj3 Title"))
        self.label_16.setText(_translate("Dialog", "Obj3 Title"))
        self.label_47.setText(_translate("Dialog", "Obj1 Title"))
        self.label_104.setText(_translate("Dialog", "Obj4 Title"))
        self.label_105.setText(_translate("Dialog", "Obj4 Title"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
