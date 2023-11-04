const { Server } = require('socket.io');
const db = require('../utils/db');

function fetchNotif(socket, token) {
    db.getNotificationsFromToken(token).then((notifications) => {
        notificationsText = []
        for (let i = 0; i < notifications.length; i++) {
            notificationsText.push(notifications[i].notificationText)
        }
        socket.emit('notifications', notificationsText);
    })
}

async function startHandler(server,app) {
    const io = new Server(server);
    io.on('connection', (socket) => {
        console.log("new socketio connection")
        socket.emit('status', 'auth');
        socket.on('auth', (token) => {
            console.log("ws auth with " + token)
            db.getUserBy("token", token).then((user) => {
                if (user) {
                    socket.emit('status', 'authSuccess');
                    fetchNotif(socket, token)
                    app.on('event:new_notification', (userToken) => {
                        if (userToken == token) {
                            fetchNotif(socket, token)
                        }
                    })
                } else {
                    socket.emit('status', 'authFail');
                }
            })
        });
        socket.on('disconnect', () => {
            console.log("socketio disconnect")
        });
    });
}

exports.startHandler = startHandler;