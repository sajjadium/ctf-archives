import WebSocket from "ws";
import { FLAG, WS_SERVER } from "./config.js";
import { isJson } from "./util.js";

const conn = new WebSocket(WS_SERVER)
const username = 'flagbot'

const handleLogin = () => {
    conn.send(JSON.stringify({ 
        api: "login", 
        username: username 
    }))
}

const handleGetFlag = (from) => {
    console.log('[getflag]', from)
    if(from === 'admin'){
        conn.send(JSON.stringify({
            api: 'sendflag',
            flag: FLAG,
            to: from
        }))
    }
}

const handleList = (list) => {
    console.log(list)
}

const handleMsg = (msg) => {
    switch(msg.api){
        case "login":
            handleLogin()
            break
        case "list":
            handleList(msg.peers)
            break
        case "getflag":
            if(msg.from) handleGetFlag(msg.from)
            break
        default:
            console.log("unknown api", msg.api)
    }
}

conn.onopen = () => {
    const msg = {
        api: "ping",
        data: "hello world"
    }
    conn.send(JSON.stringify(msg))
    conn.send(JSON.stringify({api: "list"}))
}

conn.on('message', msg => {
    console.log('[onmessage]', msg.toString())
    if(isJson(msg)){
        handleMsg(JSON.parse(msg))
    }
})