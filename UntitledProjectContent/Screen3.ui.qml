

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls

Item {
    id: root
    width: 1920
    height: 1080

    Rectangle {
        id: rectangle
        x: 270
        y: 188
        width: 1305
        height: 598
        color: "#ffffff"

        Text {
            id: _text
            x: 450
            y: 51
            text: qsTr("Update Quantity")
            font.pixelSize: 60
        }
        Rectangle {
            id: rectangle2
            x: 458
            y: 181
            width: 200
            height: 200
            color: "#a2a2a2"
        }

        Rectangle {
            id: rectangle3
            x: 693
            y: 181
            width: 200
            height: 200
            color: "#a2a2a2"
        }

        Rectangle {
            id: rectangle4
            x: 693
            y: 513
            width: 200
            height: 60
            color: "#a2a2a2"

            Text {
                id: _text1
                x: 34
                y: 12
                text: qsTr("Save Edits")
                font.pixelSize: 30
            }
        }
        Rectangle {
            id: rectangle5
            x: 458
            y: 513
            width: 200
            height: 60
            color: "#a2a2a2"

            Text {
                id: _text2
                x: 56
                y: 12
                text: qsTr("Cancel")
                font.pixelSize: 30
            }
        }

        Text {
            id: _text3
            x: 497
            y: 414
            text: qsTr(" Current
Quantity")
            font.pixelSize: 30
        }

        Text {
            id: _text4
            x: 733
            y: 414
            text: qsTr("   New
Quantity")
            font.pixelSize: 30
        }

        Button {
            id: button
            x: 931
            y: 212
            text: qsTr("Up")
            font.pixelSize: 30
        }

        Button {
            id: button1
            x: 931
            y: 296
            text: qsTr("Down")
            font.pixelSize: 30
        }
    }
}
