

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
        x: 515
        y: 253
        width: 851
        height: 502
        color: "#ffffff"

        Text {
            id: _overview
            x: 238
            y: 28
            text: qsTr("Remove Item?")
            font.pixelSize: 60
        }

        Button {
            id: cancel
            x: 66
            y: 305
            width: 295
            height: 138
            text: qsTr("Cancel")
            font.pixelSize: 60
        }
        Button {
            id: remove
            x: 466
            y: 305
            width: 295
            height: 138
            text: qsTr("Remove")
            font.pixelSize: 60
        }

        Text {
            id: _text
            x: 138
            y: 183
            text: qsTr("Are you sure you want to remove this item?")
            font.pixelSize: 30
        }

        Text {
            id: _text1
            x: 226
            y: 231
            text: qsTr("This action cannot be undone.")
            font.pixelSize: 30
        }
    }
}
