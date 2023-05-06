const fs = require("fs");

const flags = new Map();
for(let flag of JSON.parse(fs.readFileSync("flags.json")).flags) {
    if(flag.name === "corCTF") {
        flag.text = process.env.FLAG || "corctf{test_flag}";
    }
    flags.set(flag.name, flag);
}

const users = new Map();

const buyFlag = ({ flag, user }) => {
    if(!flags.has(flag)) {
        throw new Error("Unknown flag");
    }
    if(user.money < flags.get(flag).price) {
        throw new Error("Not enough money");
    }

    user.money -= flags.get(flag).price;
    user.flags.push(flag);
    users.set(user.user, user);
};

module.exports = { flags, users, buyFlag };