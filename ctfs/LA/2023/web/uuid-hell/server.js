const uuid = require('uuid');
const crypto = require('crypto')

function randomUUID() {
    return uuid.v1({'node': [0x67, 0x69, 0x6E, 0x6B, 0x6F, 0x69], 'clockseq': 0b10101001100100});
}
let adminuuids = []
let useruuids = []
let pow = []
function isAdmin(uuid) {
    return adminuuids.includes(uuid);
}
function isUuid(uuid) {
    if (uuid.length != 36) {
        return false;
    }
    for (const c of uuid) {
        if (!/[-a-f0-9]/.test(c)) {
            return false;
        }
    }
    return true;
}

function getUsers() {
    let output = "<strong>Admin users:</strong>\n";
    adminuuids.forEach((adminuuid) => {
        const hash = crypto.createHash('md5').update("admin" + adminuuid).digest("hex");
        output += `<tr><td>${hash}</td></tr>\n`;
    });
    output += "<br><br><strong>Regular users:</strong>\n";
    useruuids.forEach((useruuid) => {
        const hash = crypto.createHash('md5').update(useruuid).digest("hex");
        output += `<tr><td>${hash}</td></tr>\n`;
    });
    return output;
}

const express = require('express');
const cookieParser = require("cookie-parser");

const app = express();
app.use(cookieParser());



app.get('/', (req, res) => {
    let id = req.cookies['id'];
    if (id === undefined || !isUuid(id)) {
        id = randomUUID();
        res.cookie("id", id);
        useruuids.push(id);
        if (useruuids.length > 50) {
            useruuids.shift();
        }
    } else if (isAdmin(id)) {
        res.send(process.env.FLAG);
        return;
    }

    res.send("You are logged in as " + id + "<br><br>" + getUsers());
});

app.post('/createadmin', (req, res) => {

    const adminid = randomUUID();
    adminuuids.push(adminid);
    if (adminuuids.length > 50) {
        adminuuids.shift();
    }
    res.send("Admin account created.")
});

app.listen(process.env.PORT);