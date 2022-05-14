import QtQuick 2.12
import QtQuick.Controls 2.12
import SddmComponents 2.0
import "SimpleControls" as Simple

Rectangle {

    readonly property color backgroundColor: Qt.rgba(0, 0, 0, 0.4)
    readonly property color hoverBackgroundColor: Qt.rgba(0, 0, 0, 0.6)
    
    width: 640
    height: 480
    
    LayoutMirroring.enabled: Qt.locale().textDirection == Qt.RightToLeft
    LayoutMirroring.childrenInherit: true

    TextConstants { id: textConstants }
    
    Connections {
        target: sddm
        
        onLoginSucceeded: {}
        
        onLoginFailed: {
            pw_entry.clear()
            pw_entry.focus = true
            
            errorMsgContainer.visible = true
        }
    }
    
    Background {
        anchors.fill: parent
        source: config.background
        fillMode: Image.PreserveAspectCrop
        onStatusChanged: {
            if (status == Image.Error && source != config.defaultBackground) {
                source = config.defaultBackground
            }
        }
    }

    Column {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        spacing: 10

        Simple.ComboBox {
            id: user_entry
            model: userModel
            currentIndex: userModel.lastIndex
            textRole: "realName"
            width: 250
            KeyNavigation.backtab: session
            KeyNavigation.tab: pw_entry
        }

        TextField {
            id: pw_entry
            color: "white"
            echoMode: TextInput.Password
            focus: true
            placeholderText: textConstants.promptPassword
            width: 250
            background: Rectangle {
                implicitWidth: 100
                implicitHeight: 30
                color: pw_entry.activeFocus ? hoverBackgroundColor : backgroundColor
                border.color: Qt.rgba(1, 1, 1, 0.4)
                radius: 3
            }
            onAccepted: sddm.login(user_entry.getValue(), pw_entry.text, session.currentIndex)
            KeyNavigation.backtab: user_entry
            KeyNavigation.tab: loginButton
        }

        Simple.Button {
            id: loginButton
            text: textConstants.login
            width: 250
            onClicked: sddm.login(user_entry.getValue(), pw_entry.text, session.currentIndex)
            KeyNavigation.backtab: pw_entry
            KeyNavigation.tab: suspend
        }
        
        Rectangle {
            id: errorMsgContainer
            width: 250
            height: loginButton.height
            color: "#F44336"
            clip: true
            visible: false
            radius: 3
            
            Label {
                anchors.centerIn: parent
                text: textConstants.loginFailed
                width: 240
                color: "white"
                font.bold: true
                elide: Qt.locale().textDirection == Qt.RightToLeft ? Text.ElideLeft : Text.ElideRight
                horizontalAlignment: Qt.AlignHCenter
            }
        }

    }

    Row {
        anchors {
            bottom: parent.bottom
            bottomMargin: 10
            horizontalCenter: parent.horizontalCenter
        }

        spacing: 5
        
        Simple.Button {
            id: suspend
            text: textConstants.suspend
            onClicked: sddm.suspend()
            visible: sddm.canSuspend
            KeyNavigation.backtab: loginButton
            KeyNavigation.tab: hibernate
        }

        Simple.Button {
            id: hibernate
            text: textConstants.hibernate
            onClicked: sddm.hibernate()
            visible: sddm.canHibernate
            KeyNavigation.backtab: suspend
            KeyNavigation.tab: restart
        }
        
        Simple.Button {
            id: restart
            text: textConstants.reboot
            onClicked: sddm.reboot()
            visible: sddm.canReboot
            KeyNavigation.backtab: suspend; KeyNavigation.tab: shutdown
        }
        
        Simple.Button {
            id: shutdown
            text: textConstants.shutdown
            onClicked: sddm.powerOff()
            visible: sddm.canPowerOff
            KeyNavigation.backtab: restart; KeyNavigation.tab: session
        }
    }

    Simple.ComboBox {
        id: session
        anchors {
            left: parent.left
            leftMargin: 10
            top: parent.top
            topMargin: 10
        }
        currentIndex: sessionModel.lastIndex
        model: sessionModel
        textRole: "name"
        width: 200
        visible: sessionModel.rowCount() > 1
        KeyNavigation.backtab: shutdown
        KeyNavigation.tab: user_entry
    }

    Rectangle {
        id: timeContainer
        anchors {
            top: parent.top
            right: parent.right
            topMargin: 10
            rightMargin: 10
        }
        border.color: Qt.rgba(1, 1, 1, 0.4)
        radius: 3
        color: backgroundColor
        width: timelb.width + 10
        height: session.height

        Label {
            id: timelb
            anchors.centerIn: parent
            text: Qt.formatDateTime(new Date(), "HH:mm")
            color: "white"
            horizontalAlignment: Text.AlignHCenter
        }
    }

    Timer {
        id: timetr
        interval: 500
        repeat: true
        onTriggered: {
            timelb.text = Qt.formatDateTime(new Date(), "HH:mm")
        }
    }
    
    Component.onCompleted: print(sddm.canPowerOff)
}
