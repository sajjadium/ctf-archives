import { WebSocketServer } from "ws";
import express from "express";
import { createServer } from "http";
import bodyParser from 'body-parser'
import fs from 'fs';
import { v4 as uuidv4 } from 'uuid';
import path from "path";
import { PORT, LISTEN } from "./config.js";
import { fileURLToPath } from "url";


const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const app = express()
const http = createServer(app)
const TPL_PATH = './tpls'

app.use(bodyParser.json())
app.use(express.static(path.join(__dirname, 'public')))

app.get('/hello', (req, res) => {
    res.send("hello world");
})

app.post('/tplCreate', (req, res) => {
    const tpl = req.body.tpl
    if(!tpl){
        res.send('no tpl field specified!')
        return
    }
    const tplName = uuidv4() + '.tpl'
    fs.writeFile(path.join(TPL_PATH, tplName), tpl, () => {
        res.json({ 'tplID': tplName })
    })
})

app.get('/tplView', (req, res) => {
    const tplName = req.query.tpl
    if(!tplName || !tplName.endsWith('.tpl')){
        res.send('wrong tpl id!')
        return
    }
    res.header('Content-Type', 'text/html')
    res.sendFile(path.join(__dirname, TPL_PATH, tplName), (err) => {
        if(err) res.send(err)
    })
})

app.get('/tplList', (req, res) => {
    res.json(fs.readdirSync(TPL_PATH))
})

app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const wss = new WebSocketServer({ server: http })

const clients = new Map()
const ws2username = new Map()
const username2ws = new Map()

const sendWarning = (ws, warning) => {
    ws.send(JSON.stringify({
        api: 'warning',
        warning: warning
    }))
}

const apiPing = (ws) => { ws.send('pong') }

const apiList = (ws) => { 
    ws.send(JSON.stringify({
        api: 'list',
        peers: Array.from(username2ws.keys())
    })) 
}

const apiSendmsg = (ws, content, to) => {
    if(!username2ws.has(to)){ 
        return 
    }
    // console.log(ws2username)
    if(content.type == 'tpl'){
        let tplfile = path.join(TPL_PATH, content.data.tpl)
        if(!tplfile.endsWith('.tpl')){
            tplfile += '.tpl'
        }
        content.data.tpl = fs.existsSync(tplfile) ? fs.readFileSync(tplfile).toString() : '***'
    }
    username2ws.get(to).send(JSON.stringify({
        api: "message", 
        from: ws2username.get(ws), 
        content: content
    }))
}

const apiLogin = (ws, username) => {
    console.log(username)
    ws2username.set(ws, username)
    if(username2ws.has(username)){
        console.log(username, "logged in already")
        sendWarning(ws, 'username already used!')
        ws.close()
        return
        // username2ws.get(username).close()
    }
    username2ws.set(username, ws)
    ws.send(`Now you are ${username}`)
}

const apiSendFlag = (ws, flag, to) => {
    username2ws.get(to).send(JSON.stringify({
        api: "flag",
        flag: flag
    }))
}

const apiGetFlag = (ws) => {
    username2ws.get('flagbot').send(JSON.stringify({
        api: "getflag",
        from: ws2username.get(ws)
    }))
}

const handleMsg = (msg, ws) => {
    switch(msg.api){
        case "login":
            apiLogin(ws, msg.username)
            break
        case "ping":
            apiPing(ws)
            break
        case 'list':
            apiList(ws)
            break
        case 'sendmsg':
            apiSendmsg(ws, msg.msg, msg.to)
            break
        case 'sendflag':
            apiSendFlag(ws, msg.flag, msg.to)
            break
        case 'getflag':
            apiGetFlag(ws)
            break
        default:
            console.log('unknown api')
    }
}

const handleConn = (ws, addr) => {
    // console.log(typeof ws)
    ws.send(JSON.stringify({ api: "login" })) // login required
    setTimeout(() => {
        if(!ws2username.has(ws)) ws.close()
    }, 5000)
    
    ws.on('message', msg => {
        const data = JSON.parse(msg)
        console.log(data)
        handleMsg(data, ws)
    })
    ws.on('close', () => {
        const username = ws2username.get(ws)
        console.log(addr, username, "closed")
        clients.delete(addr)
        username2ws.delete(username)
        ws2username.delete(ws)
    })
    ws.on('ping', () => {
        ws.send('pong')
        console.log('ping')
    })
}

wss.on('connection', (ws, req) => {
    const { remoteAddress:host, remotePort:port } = req.socket 
    console.log(host, port)
    clients.set(`${host}:${port}`, ws)
    handleConn(ws, `${host}:${port}`)
})

// wss.on('listening', () => {
//     console.log('listening...')
// })

http.listen(PORT, LISTEN, () => {
    console.log(`listening on ${LISTEN}:${PORT}`);
});