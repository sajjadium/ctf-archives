import express from 'express'
import { WebSocketServer, WebSocket } from 'ws'
import { createServer } from 'http'
import { renderFile } from 'ejs'
import {NUM_PLATES, PORT, TICK_INTERVAL} from './util/constants.js'
import PlayerContext from './states/player-context.js'
import { generateRandomPlate, isValidVIN } from './util/util.js';

let app = express();

app.set('views', 'src/views')
app.set('view engine', 'ejs');
app.engine('html', renderFile);
app.use('/static', express.static('src/static'))


app.get('/', (req, res) => {
    const vin = req.query.vin;
    if (!vin) {
        res.send("plz gibe VIN");
        return;
    } else if (typeof vin !== "string") {
        res.send("plz VIN must be string");
        return;
    } else if (!isValidVIN(vin)) {
        res.send("plz vin must match ^[A-Z0-9]{17}$");
        return;
    }
    const randomPlates = [];
    for (let i = 0; i < NUM_PLATES; i++) {
        randomPlates.push(generateRandomPlate());
    }
    res.render("index.ejs", { plates: randomPlates, vin: vin, port: PORT })
});

app.get('/healthz', (req, res) => {
    res.send('ok');
});

const server = createServer(app);

const wss = new WebSocketServer({ noServer: true });

server.on('upgrade', (request, socket, head) => {
    wss.handleUpgrade(request, socket, head, (ws) => {
        wss.emit('connection', ws, request);
    });
});

let activeUsers: Map<WebSocket, PlayerContext> = new Map();

wss.on('connection', (ws) => {
    ws.on('message', (message) => {
        const exists = activeUsers.get(ws);
        if (exists) {
            exists.handleMessage(message.toString())
        } else {
            try {
                activeUsers.set(ws, new PlayerContext(ws, message.toString()));
            } catch (e) {
                ws.send("cannot process message")
            }
        }
    })

    ws.on('close', () => {
        const exists = activeUsers.get(ws);
        if (exists) {
            exists.earlyTerminate();
        }
    });
});

const loop = setInterval(() => {
    for (const [ws, user] of activeUsers.entries()) {
        if (user.isConnectionClosed()) {
            activeUsers.delete(ws);
        } else {
            user.nextTick();
        }
    }
}, TICK_INTERVAL);

export {
    server,
    wss,
    loop,
}