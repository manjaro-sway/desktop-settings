import QtQuick 2.12
import QtQuick.Controls 2.12

Button {
    id: control

    contentItem: Text {
        text: control.text
        font: control.font
        color: "white"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    background: Rectangle {
        implicitWidth: 100
        implicitHeight: 30
        color: control.down ? Qt.rgba(0, 0, 0, 0.6) : Qt.rgba(0, 0, 0, 0.4)
        border.color: Qt.rgba(1, 1, 1, 0.4)
        border.width: 1
        radius: 3
    }
}
