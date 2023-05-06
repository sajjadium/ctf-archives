const { Server, WebSocket } = require('ws');
const jwt = require('jsonwebtoken');
const wss = new Server({ port: 7071 });
const {randomBytes} = require("crypto")
const fs = require("fs");
const request = require('request');

const privateKey = fs.readFileSync('private.key');
const publicKey = fs.readFileSync('public.key');

let locationMap = new Map();
const secretKey = "[REPLACE ME]"
const FLAG = "we{test}"
const boardSize = 32;
const boardMinWalkDistance = Math.sqrt(Math.pow(boardSize, 2) + Math.pow(boardSize, 2));

const USERNAMES = {}

// get current time in second
const currentTime = () => {
    return Date.now() / 1000
}

// verify recaptcha
function verify_recaptcha_token(token, callback){
    request("https://www.google.com/recaptcha/api/siteverify?secret=" + secretKey + "&response=" + token,function(error,response,body) {
        body = JSON.parse(body);
        callback(body.success)
    });
}

// ensure coord is greater than 0 and smaller than boardSize
const normalizeBoundary = (coordXY) => {
    coordXY = coordXY > 0 ? coordXY : 0;
    coordXY = coordXY < boardSize ? coordXY : boardSize - 1;
    return coordXY
}

// change position based on action
const changePos = (pos, direction) => {
    pos.y += direction === "up" ? -1 : direction === "down" ? 1 : 0;
    pos.x += direction === "left" ? -1 : direction === "right" ? 1 : 0;
    return {
        x: normalizeBoundary(pos.x),
        y: normalizeBoundary(pos.y)
    }
}

// determine whether is dino dead
const isDead = (pos) => {
    let {x, y} = pos;
    const distance = Math.sqrt(Math.pow(boardSize - x, 2) + Math.pow(boardSize - y, 2));
    const travelPercentage = 1 - distance / boardMinWalkDistance;
    if (Math.random() < travelPercentage) return true;
    if (travelPercentage > 0.5) { // just to make rest of the trip extra hard
        if (Math.random() < 0.99) {
            return true;
        }
    }
    return false;
}

// routinely broadcast all dinos location
setInterval(()=>{
    let locations = [];
    const toDeletes = [];
    const currentTimestamp = currentTime();
    locationMap.forEach((v, k) => {
        if (currentTimestamp - v.lastMove > 300) // inactive dinos are removed
            toDeletes.push(k)
        if (v.x !== 0 || v.y !== 0) // dinos at (0,0) are not broadcasted
            locations.push(v)
    })
    // delete all inactive dinos
    toDeletes.forEach((k) => locationMap.delete(k));
    locations = locations.slice(0, 100)
    // console.log("sending", locations, "deleted", toDeletes, "broadcasted", wss.clients.size, "at", currentTimestamp);
    wss.clients.forEach(function each(client) {
        if (client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify({
                command: "state",
                locations: locations,
                success: true
            }));
        }
    });
}, 1000)

wss.on('connection', (ws) => {
    ws.on('message', (messageAsString) => {
        const messages = JSON.parse(messageAsString)
        switch (messages.command) {
            case "create": // create a dino
                verify_recaptcha_token(messages.captcha, (correct) => {
                    if (correct) {
                        const usernameB64 = Buffer.from(messages.name).toString("base64");
                        if (USERNAMES[usernameB64] !== undefined) {
                            return ws.send(JSON.stringify({
                                success: false, msg: "username taken"
                            }))
                        }
                        USERNAMES[usernameB64] = true;
                        const key = randomBytes(32).toString("base64")
                        locationMap.set(key, {x: 0, y: 0, lastMove: currentTime(), name: messages.name, dino: messages.dino})
                        const token = jwt.sign({
                            position: {x: 0, y: 0}, dead: false, key, name: messages.name
                        }, privateKey, { algorithm: 'RS256'});
                        return ws.send(JSON.stringify({
                            command: "set_token",
                            token,
                            dead: false,
                            success: true,
                        }))
                    }
                    return ws.send(JSON.stringify({
                        success: false, msg: "recaptcha wrong"
                    }))
                })
                break
            case "up":
            case "down":
            case "left":
            case "right":
                try {
                    const decoded = jwt.verify(messages.token, publicKey, { algorithm: 'RS256'});
                    if (decoded.dead) {
                        return ws.send(JSON.stringify({
                            success: false,
                            msg: "your dino is dead"
                        }))
                    }
                    let position = changePos(decoded.position, messages.command);
                    const dead = isDead(position)
                    position = dead ? {x: 0, y: 0} : position
                    if (dead) {
                        locationMap.delete(decoded.key)
                        return ws.send(JSON.stringify({
                            command: "set_token",
                            dead: true,
                            success: true,
                        }))
                    } else {
                        let item = locationMap.get(decoded.key) || {};
                        item.x = position.x
                        item.y = position.y
                        item.lastMove =  currentTime()
                    }

                    const token = jwt.sign({
                        position, dead, key: decoded.key, name: messages.name
                    }, privateKey, { algorithm: 'RS256'});
                    return ws.send(JSON.stringify({
                        command: "set_token",
                        token,
                        dead,
                        flag: (position.x === boardSize - 1 && position.y === boardSize - 1 && !dead) ? FLAG : "",
                        success: true,
                    }))
                } catch(err) {
                    console.log(err)
                }
        }
    });
    ws.on("close", () => {
    });
});



