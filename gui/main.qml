import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts 6.0
import QtQuick.Controls.Material
import QtQuick.Dialogs
import Qt.labs.platform

import Qt5Compat.GraphicalEffects


Window {
    id: window
    title: "ShedevrumMonitor"
    visible: true

    minimumWidth: 700
    minimumHeight: 550
    color: "#161616"
    Material.theme: Material.Dark
    Material.accent: "#FF5722"

    Component.onCompleted: {
        animation.paused = false
        update_data()
        update_user_data()
    }

    Connections {
        target: Monitor

        function onDataUpdated() {
            window.update_data()
        }

        function onUserDataUpdated() {
            window.update_user_data()
        }
    }

    function update_data() {
        subscriptions.text = Monitor.get_subscriptions()
        subscribers.text = Monitor.get_subscribers()
        likes.text = Monitor.get_likes()
    }

    function update_user_data() {
        username.text = Monitor.get_display_name()

        let url = Monitor.get_avatar_link()
        if (url !== '') avatar.source = Monitor.get_avatar_link()
    }

    AnimatedImage {
        id: animation
        anchors.fill: parent
        source: "images/intro.gif"
        currentFrame: 111
        paused: true
        opacity: 1
        z: 10

        onCurrentFrameChanged: {
            if (currentFrame === frameCount - 1) {
                opacity = 0
                subscribers_gif.paused = false
                likes_gif.paused = false
                subscribes_gif.paused = false
            }
        }

        Behavior on opacity {
            NumberAnimation {
                duration: 600
            }
        }
    }

    Item {
        anchors.fill: parent

        AnimatedImage {
            id: background_gif
            anchors.fill: parent
            source: "images/background.gif"
            opacity: 0.2
        }

        AnimatedImage {
            id: avatar_gif
            x: (parent.width - width) / 2
            y: 20
            width: 400
            height: 300
            source: "images/avatar.gif"

            Rectangle {
                id: mask
                height: parent.height - 210
                width: height
                color: 'green'
                radius: height
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                visible: false
            }

            Image {
                id: avatar
                anchors.fill: parent
                source: "images/islands-retina-50.jpg"
                z: 20
                visible: false
            }

            OpacityMask {
                id: opacityMask
                anchors.fill: mask
                source: avatar
                maskSource: mask
            }

            Text {
                id: username
                text: ''
                color: 'white'
                anchors.horizontalCenter: parent.horizontalCenter
                y: parent.y + 25
                font.pixelSize: 20

                Button {
                    anchors.left: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.leftMargin: 10
                    text: 'Изменить'
                    flat: true

                    onClicked: set_username_popup.open()
                }
            }
        }

        AnimatedImage {
            id: subscribers_gif
            x: 20
            y: parent.height / 3
            width: 270
            height: 270
            source: "images/secondary.gif"
            currentFrame: 10
            paused: true

            Text {
                id: subscriptions
                text: '3.6k'
                color: 'white'
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: 30
            }

            Text {
                text: 'Подписки'
                color: 'white'
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 40
                font.pixelSize: 20
            }
        }

        AnimatedImage {
            id: likes_gif
            x: (parent.width - width) / 2
            y: parent.height - height - 20
            width: 270
            height: 270
            source: "images/secondary.gif"
            currentFrame: 15
            paused: true

            Text {
                id: likes
                text: '23.2k'
                color: 'white'
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: 30
            }

            Text {
                text: 'Лайки'
                color: 'white'
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 40
                font.pixelSize: 20
            }
        }

        AnimatedImage {
            id: subscribes_gif
            x: parent.width - width - 20
            y: parent.height / 3
            width: 270
            height: 270
            source: "images/secondary.gif"
            currentFrame: 20
            paused: true

            Text {
                id: subscribers
                text: '2.6k'
                color: 'white'
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: 30
            }

            Text {
                text: 'Подписчиков'
                color: 'white'
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 40
                font.pixelSize: 20
            }
        }
    }


    Popup {
        id: set_username_popup
        x: h_paddings / 2
        y: v_paddings / 2
        width: parent.width - h_paddings
        height: 65
        modal: true

        property real h_paddings: 100
        property real v_paddings: 500

        function set_username() {
            Monitor.set_username(_username.text)
            set_username_popup.close()
        }

        contentItem: Row {
            spacing: 10

            TextField {
                id: _username
                placeholderText: 'ID или имя пользователя'
                width: parent.width - set_username_button.width - parent.spacing
                height: 40

                onAccepted: set_username_popup.set_username()
            }

            Button {
                id: set_username_button
                text: 'Применить'
                enabled: _username.text != ''
                anchors.verticalCenter: _username.verticalCenter
                onClicked: set_username_popup.set_username()
            }
        }
    }
}
