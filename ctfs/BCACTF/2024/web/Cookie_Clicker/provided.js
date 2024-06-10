const express = require('express')
const app = express();

const http = require('http').Server(app);

const port = 3000;

const socketIo = require('socket.io');
const io = socketIo(http);


let sessions = {}
let errors = {}

app.use(express.static(__dirname));

app.get('/', (req, res) => {
    res.sendFile("./index.html")
})

io.on('connection', (socket) => {
    sessions[socket.id] = 0
    errors[socket.id] = 0

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });

    socket.on('chat message', (msg) => {
        socket.emit('chat message', msg);
    });

    socket.on('receivedError', (msg) => {
        sessions[socket.id] = errors[socket.id]
        socket.emit('recievedScore', JSON.stringify({"value":sessions[socket.id]}));
    });

    socket.on('click', (msg) => {
        let json = JSON.parse(msg)

        if (sessions[socket.id] > 1e20) {
            socket.emit('recievedScore', JSON.stringify({"value":"FLAG"}));
            return;
        }

        if (json.value != sessions[socket.id]) {
            socket.emit("error", "previous value does not match")
        }

        let oldValue = sessions[socket.id]
        let newValue = Math.floor(Math.random() * json.power) + 1 + oldValue

        sessions[socket.id] = newValue
        socket.emit('recievedScore', JSON.stringify({"value":newValue}));

        if (json.power > 10) {
            socket.emit('error', JSON.stringify({"value":oldValue}));
        }

        errors[socket.id] = oldValue;
    });
});

http.listen(port, () => {
    console.log(`App server listening on ${port}. (Go to http://localhost:${port})`);
});