const express = require('express');
const crypto = require("crypto");
const https = require('https');
const fs = require('fs');

const app = express();
app.use(express.json({ limit: '1kb' }));
app.use(express.urlencoded({ extended: false }));

const BOT_HOST = process.env.BOT_HOST || 'localhost';
const BOT_PORT = process.env.BOT_PORT || 7777;

const db = new Map();

app.get("/", function (_, res) {
    res.sendFile(__dirname + '/html/index.html')
});

app.get("/message/:id", function (_, res) {
    res.sendFile(__dirname + '/html/message.html')
});

app.put("/api/message", function (req, res) {
    const content = req.body.message;
    if (typeof content !== 'string') return res.json({ error: "Invalid message" });
    const id = crypto.randomBytes(12).toString('base64url');
    db.set(id, content);
    res.json({ id });
});

app.get("/api/message/:id", function (req, res) {
    const content = db.get(req.params.id) || '(destructed)';
    db.delete(req.params.id);
    res.json({ content });
});


// bot stuff below

const net = require('net');
const hcaptcha = require('./hcaptcha');

app.get("/report", function (req, res) {
    res.sendFile(__dirname + "/html/report.html");
});

app.post("/report", hcaptcha, function (req, res) {
    const { url } = req.body;
    if (!url || !RegExp(`^https?://${req.hostname.replace('.', '\\.')}/`).test(url)) {
        return res.status(400).send('Invalid URL');
    }
    console.log(`[+] Sending ${url} to bot`)
    try {
        const client = net.connect(BOT_PORT, BOT_HOST, () => {
            client.write(url)
        })

        let response = ''
        client.on('data', data => {
            response += data.toString()
            client.end()
        })

        client.on('end', () => res.send(response))
    } catch (e) {
        console.log(e)
        res.status(500).send('Something is wrong...')
    }
});

if (process.env.HTTPS) {
    const key = fs.readFileSync('/opt/credentials/privkey.pem', 'utf8');
    const cert = fs.readFileSync('/opt/credentials/cert.pem', 'utf8');
    const ca = fs.readFileSync('/opt/credentials/chain.pem', 'utf8');

    const credentials = { key, cert, ca };
    const httpsServer = https.createServer(credentials, app);
    httpsServer.listen(48763);
} else {
    // for testing
    app.listen(8763);
}
