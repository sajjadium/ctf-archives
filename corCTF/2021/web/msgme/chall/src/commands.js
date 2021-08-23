const fs = require('fs');

let cmdList = [
    "help",
    "roll",
    "secret",
    "8ball",
    "math",
    "coinflip",
    "flag"
];
let cmds = Object.create(null);

const init = () => {
    for(let i = 0; i < cmdList.length; i++) {
        let name = cmdList[i];
        let cmd = require(`./commands/${name}.js`);
        cmds[name] = cmd;
    }
}

const handle = (ws, data) => {
    let args = data.msg.split(" ");
    let cmd = args[0].slice(1);
    data.msg = `${ws.user}: `;

    let found = false;
    for(let name of Object.keys(cmds)) {
        if(cmd.includes(name)) {
            found = true;
            cmds[name].run(ws, args, data);
        }
    }

    if(found) {
        return data;
    }
    return false;
};

module.exports = { cmds, init, handle };