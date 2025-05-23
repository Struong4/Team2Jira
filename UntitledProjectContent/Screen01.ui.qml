

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import UntitledProject

Rectangle {
    width: Constants.width
    height: Constants.height
    color: Constants.backgroundColor

    Rectangle {
        id: _SearchHolder
        x: 57
        y: 58
        width: 650
        height: 63
        color: "#ffffff"
        border.width: 5
    }

    Text {
        id: _SearchBar
        x: 65
        y: 70
        text: qsTr("Search by keyword")
        font.pixelSize: 30
    }

    Rectangle {
        id: _MenuBox
        x: 57
        y: 160
        width: 1810
        height: 826
        color: "#ffffff"
        border.width: 2

        Rectangle {
            id: _categoryBox
            x: 2
            y: 98
            width: 1810
            height: 78
            border.width: 2

            Text {
                id: _categorys
                x: 46
                y: 15
                width: 1511
                height: 34
                text: qsTr("ID                     Name                    Category                    Current Stock                Update Quantity                Action")
                font.pixelSize: 30
            }
        }

        Rectangle {
            id: firstBox
            x: 0
            y: 182
            width: 1810
            height: 160
            color: "#ffffff"
            border.width: 2

            Rectangle {
                id: firstNameBox
                x: 149
                y: 39
                width: 282
                height: 83
                color: "#ffffff"
                border.width: 2
            }

            Rectangle {
                id: firstTypeBox
                x: 465
                y: 39
                width: 230
                height: 83
                color: "#ffffff"
                border.width: 2
            }

            Rectangle {
                id: firstQuantBox
                x: 805
                y: 39
                width: 120
                height: 83
                color: "#ffffff"
                border.width: 2
            }

            Rectangle {
                id: firstNQBox
                x: 1105
                y: 39
                width: 180
                height: 83
                color: "#ffffff"
                border.width: 2
            }

            Button {
                id: button1
                x: 1433
                y: 54
                text: qsTr("Update?")
            }
        }

        Rectangle {
            id: secondBox
            x: 0
            y: 345
            width: 1810
            height: 160
            color: "#ffffff"
            border.width: 2

            Text {
                id: _idFirst
                x: 31
                y: -111
                text: qsTr("001")
                font.pixelSize: 40
            }

            Text {
                id: _idSecond
                x: 31
                y: 53
                text: qsTr("002")
                font.pixelSize: 40
            }

            Rectangle {
                id: secondNameBox
                x: 149
                y: 39
                width: 282
                height: 83
                color: "#ffffff"
                border.width: 1
            }

            Rectangle {
                id: secondTypeBox
                x: 465
                y: 39
                width: 230
                height: 83
                color: "#ffffff"
                border.width: 2
            }

            Rectangle {
                id: secondQuantBox
                x: 805
                y: 39
                width: 120
                height: 83
                color: "#ffffff"
                border.width: 2
            }

            Rectangle {
                id: secondNQBox
                x: 1105
                y: 39
                width: 180
                height: 83
                color: "#ffffff"
                border.width: 2
            }

            Button {
                id: button2
                x: 1433
                y: 54
                text: qsTr("Update?")
            }
        }

        Rectangle {
            id: thirdBox
            x: 0
            y: 507
            width: 1810
            height: 160
            color: "#ffffff"
            border.width: 2

            Text {
                id: _idThird
                x: 31
                y: 53
                text: qsTr("003")
                font.pixelSize: 40
            }

            Rectangle {
                id: thirdNameBox
                x: 149
                y: 39
                width: 282
                height: 83
                color: "#ffffff"
                border.width: 1
            }

            Rectangle {
                id: thirdTypeBox
                x: 465
                y: 39
                width: 230
                height: 83
                color: "#ffffff"
                border.width: 2
            }

            Rectangle {
                id: thirdQuantBox
                x: 805
                y: 39
                width: 120
                height: 83
                color: "#ffffff"
                border.width: 2
            }

            Rectangle {
                id: thirdNQBox
                x: 1105
                y: 39
                width: 180
                height: 83
                color: "#ffffff"
                border.width: 2
            }

            Button {
                id: button3
                x: 1433
                y: 54
                text: qsTr("Update?")
            }
        }

        Rectangle {
            id: fourthBox
            x: 0
            y: 670
            width: 1810
            height: 160
            color: "#ffffff"
            border.width: 2

            Text {
                id: _idFourth
                x: 31
                y: 53
                text: qsTr("004")
                font.pixelSize: 40
            }

            Rectangle {
                id: fourthNameBox
                x: 149
                y: 39
                width: 282
                height: 83
                color: "#ffffff"
                border.width: 2
            }

            Rectangle {
                id: fourthTypeBox
                x: 465
                y: 39
                width: 230
                height: 83
                color: "#ffffff"
                border.width: 2
            }

            Rectangle {
                id: fourthQuantBox
                x: 805
                y: 39
                width: 120
                height: 83
                color: "#ffffff"
                border.width: 2
            }

            Rectangle {
                id: fourthNQBox
                x: 1105
                y: 39
                width: 180
                height: 83
                color: "#ffffff"
                border.width: 2
            }

            Button {
                id: button4
                x: 1433
                y: 54
                text: qsTr("Update?")
            }
        }

        Image {
            id: image
            x: 1086
            y: 12
            width: 72
            height: 83
            source: "../../../../Downloads/go-back-icon-512x512-hqhqt5j0.png"
            fillMode: Image.PreserveAspectFit
        }

        Image {
            id: image1
            x: 1211
            y: 12
            width: 72
            height: 83
            source: "../../../../Downloads/go-forward-icon-512x512-hqhqt5j0.png"
            fillMode: Image.PreserveAspectFit
        }
    }

    Rectangle {
        id: editsBox
        x: 1598
        y: 183
        width: 237
        height: 60
        color: "#c0c0c0"
    }
    Text {
        id: _SaveEdits
        x: 1655
        y: 191
        width: 237
        height: 45
        text: qsTr("Save Edits")
        font.pixelSize: 30
    }

    Rectangle {
        id: _CancelBox
        x: 1409
        y: 183
        width: 165
        height: 60
        color: "#c0c0c0"

        Text {
            id: _Cancel
            x: 38
            y: 10
            width: 149
            height: 40
            text: qsTr("Cancel")
            font.pixelSize: 30
        }
    }
}
