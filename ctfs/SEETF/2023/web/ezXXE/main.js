const express = require('express');
const fileUpload = require('express-fileupload');
const session = require('express-session');
const FileStore = require('session-file-store')(session);
const crypto = require('crypto');
const libxmljs = require("libxmljs");

const FLAG = process.env.FLAG || "SEE{fake_flag}"
delete process.env.FLAG

const PIGEONS = require("./pigeons.json")

const BLACKLIST = [
    /<!DOCTYPE/i,
    /<!ENTITY/i,
    /SYSTEM/i,
    /PUBLIC/i
]

const validateXML = (xml) => {
    for (const regex of BLACKLIST) {
        if (regex.test(xml)) {
            return false
        }
    }
    return /^<\?xml version="1.0"/.test(xml)
}

const removePigeonsWithFlag = (pigeons) => {
    const flagRegex = /SEE{\w{60}}/ig

    let cleanPigeons = []
    for (const pigeon of pigeons) {
        if (
            !flagRegex.test(pigeon.name) &&
            !flagRegex.test(pigeon.image) &&
            !flagRegex.test(pigeon.description) &&
            !flagRegex.test(pigeon.website)
        )
            cleanPigeons.push(pigeon)
    }
    return cleanPigeons
}

const app = express()
app.use(fileUpload())
app.use(express.static('static'))

app.use(session({
    store: new FileStore(),
    secret: crypto.randomBytes(64).toString('hex'),
    resave: false,
    saveUninitialized: false,
}))

app.use((req, res, next) => {
    if (!req.session.flag) {
        req.session.flag = FLAG
    }
    next()
})

app.get("/api/pigeons", (req, res) => {
    if (!req.session.pigeons) {
        req.session.pigeons = PIGEONS
    }
    res.json(removePigeonsWithFlag(req.session.pigeons))
})

app.post("/api/export", (req, res) => {
    if (!req.session.pigeons) {
        res.status(400).send("No pigeons to export")
        return
    }
    const doc = new libxmljs.Document();
    const root = doc.node('pigeons');
    for (const pigeon of removePigeonsWithFlag(req.session.pigeons)) {
        const node = root.node('pigeon');
        node.node('name', pigeon.name);
        node.node('image', pigeon.image);
        node.node('description', pigeon.description);
        node.node('website', pigeon.website);
    }

    res.set('Content-Type', 'text/xml');
    res.send(doc.toString());
})

app.post("/api/import", (req, res) => {
    const xml = req.files.file.data

    if (!validateXML(xml)) {
        res.status(400).send("Invalid XML");
        return;
    }

    let doc;
    try {
        doc = libxmljs.parseXml(xml, { noent: true, nonet: true });
    } catch (e) {
        res.status(400).send("Invalid XML");
        return;
    }

    const pigeons = [];
    for (const node of doc.root().childNodes()) {
        if (node.name() !== 'pigeon') {
            continue;
        }
        const pigeon = {};
        if (!node.get('name') || !node.get('image') || !node.get('description') || !node.get('website')) {
            res.status(400).send("Invalid XML");
            return;
        }
        pigeon.name = node.get('name').text();
        pigeon.image = node.get('image').text();
        pigeon.description = node.get('description').text();
        pigeon.website = node.get('website').text();
        pigeons.push(pigeon);
    }
    req.session.pigeons = pigeons;
    res.send("OK");
})

app.listen(3000, () => {
    console.log('Server listening on port 3000')
})