const commands = require("./commands.js");

let ws;
const init = (wsInstance) => {
    ws = wsInstance;
    commands.init();
};

const getUser = (user) => {
    return Array.from(ws.clients).find(c => c.user === user);
};

const sendMessage = (from, to, msg) => {
    if(!from || !to || !msg || !getUser(from)) return;

    if(from !== to) {
        let connections = Array.from(ws.clients);
        connections.forEach(s => {
            if(s.user === to) {
                s.send(JSON.stringify({ from, to, msg }));
            }
        });
    }
    
    if(msg.startsWith("!")) {
        let resp = commands.handle(getUser(from), {
            from,
            to,
            msg
        });
        if(resp) {
            resp.system = true;
            getUser(from).send(JSON.stringify(resp));
            if(from !== to) {
                getUser(to)?.send(JSON.stringify(resp));
            }
        }
    }
};

module.exports = { init, getUser, sendMessage };