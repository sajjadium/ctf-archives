const express = require('express');
const jwt = require('jsonwebtoken');
const path = require('path');
const cookieParser = require('cookie-parser');
const fs = require('fs');

const secret = 'seeeeecret';

const port = 3000;
const app = express();
require('express-ws')(app);
app.use(cookieParser());
app.use((req, res, next) => {
    if ('token' in req.cookies) {
        try {
            let token = jwt.verify(req.cookies.token, secret, { algorithms: ['HS256'] });
            req.token = token;
            next();
        } catch (err) {
            return res.sendStatus(401);
        }
    } else {
        let token = { cooldown: 10 };
        req.token = token;
        let expires = new Date();
        expires.setFullYear(expires.getFullYear() + 1);
        res.cookie('token', jwt.sign(token, secret, { algorithm: 'HS256' }), {
            expires,
            httpOnly: true,
            sameSite: 'strict',
        });
        next();
    }
});

let canvas = new Uint8Array(400 * 400);
let placers = Array(400).fill(Array(400).fill(null))

function leftPad(string, pad, length) {
    while (string.length < length) {
        string = pad + string;
    }
    return string;
}
function setPixel(x, y, color, ws, cooldown) {
    console.log(`setting pixel at ${x},${y} to ${color}`);
    try {
        let packet = Buffer.alloc(7 + color.length);
        packet.writeUInt8(4, 0);
        packet.write(x, 1);
        packet.write(y, 4);
        packet.write(color, 7);
        placers[JSON.parse(x)][JSON.parse(y)].send(packet);
    } catch (err) {}
    try {
        x = JSON.parse(x);
        y = JSON.parse(y);
        if (x > 0 && x < 400 && y > 0 && y < 400 && palette.indexOf(JSON.parse(color)) != -1) {
            if (!('lastPixelPlacedTime' in ws) || Date.now() - ws.lastPixelPlacedTime > cooldown * 1000) {
                ws.lastPixelPlacedTime = Date.now();
                canvas[y * 400 + x] = palette.indexOf(JSON.parse(color));
                let packet = Buffer.alloc(7 + color.length);
                packet.writeUInt8(2, 0);
                packet.write(leftPad(String(x), ' ', 3), 1);
                packet.write(leftPad(String(y), ' ', 3), 4);
                packet.write(color, 7);
                for (let c of clients) {
                    c.send(packet);
                }
                return true;
            }
        }
    } catch (err) {
        console.error(err);
    }
    return false;
}

let palette = ['white', 'red', 'darkred', 'deeppink', 'gold', 'goldenrod', 'lime', 'seagreen', 'cyan', 'cornflowerblue', 'darkviolet', 'grey', 'dimgrey', 'black'];

app.get('/flag', (req, res) => {
    if ('admin' in req.token && req.token.admin) {
        return res.sendFile(__dirname + '/flag.txt');
    }
    return res.sendStatus(401);
});

app.get('/', (req, res) => {
    res.render('index', { palette });
});

let clients = [];

app.ws('/', (ws, req) => {
    clients.push(ws);
    ws.on('message', (data) => {
        try {
            let str = data.toString();
            let x = str.slice(0, 3);
            let y = str.slice(3, 6);
            let color = str.slice(6);
            if (setPixel(x, y, color, ws, req.token.cooldown)) {
                placers[JSON.parse(x)][JSON.parse(y)] = ws;
                ws.send(Buffer.from([3]));
            }
        } catch (err) {
            console.error(err);
        }
    });
    ws.on('close', () => {
        for (let i = 0; i < clients.length; i++) {
            if (clients[i] == ws) {
                clients.splice(i, 1);
                break;
            }
        }
    });
    let buf = Buffer.allocUnsafe(canvas.length + 1);
    buf.writeUint8(1);
    buf.set(canvas, 1);
    ws.send(buf);
});

app.set('views', './templates');
app.set('view engine', 'ejs');
app.use('/static', express.static(path.join(__dirname, 'static')));

function backupCanvas() {
    fs.writeFileSync('canvas/canvas', canvas);
    console.log(`backed up canvas at ${new Date()}`);
}
if (fs.existsSync('canvas/canvas')) {
    canvas = new Uint8Array(fs.readFileSync('canvas/canvas'));
}
app.listen(port, () => {
    console.log(`Listening on port ${port}`);
    setInterval(backupCanvas, 10000);
});
