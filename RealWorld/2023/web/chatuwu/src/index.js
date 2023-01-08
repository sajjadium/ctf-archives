const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const DOMPurify = require('isomorphic-dompurify');

const hostname = process.env.HOSTNAME || '0.0.0.0';
const port = process.env.PORT || 8000;
const rooms = ['textContent', 'DOMPurify'];


app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

io.on('connection', (socket) => {
    let {nickname, room} = socket.handshake.query;
    if (!rooms.includes(room)) {
        socket.emit('error', 'the room does not exist');
        socket.disconnect(true);
        return;
    }
    socket.join(room);
    io.to(room).emit('msg', {
        from: 'system',
        // text: `${nickname} has joined the room`
        text: 'a new user has joined the room'
    });
    socket.on('msg', msg => {
        msg.from = String(msg.from).substr(0, 16)
        msg.text = String(msg.text).substr(0, 140)
        if (room === 'DOMPurify') {
            io.to(room).emit('msg', {
                from: DOMPurify.sanitize(msg.from),
                text: DOMPurify.sanitize(msg.text),
                isHtml: true
            });
        } else {
            io.to(room).emit('msg', {
                from: msg.from,
                text: msg.text,
                isHtml: false
            });
        }
    });
});

http.listen(port, hostname, () => {
    console.log(`ChatUWU server running at http://${hostname}:${port}/`);
});