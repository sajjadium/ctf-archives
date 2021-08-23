const exec = require('child_process').exec;
const express = require('express');
const ytdl = require('ytdl-core');
const bodyParser = require('body-parser');

const app = express();
const PORT = 8000;

let prev;
let prevData;

app.use(bodyParser.json());

app.use((req, res, next) => {
    if(!req.connection.remoteAddress.includes("192.168.0.4")) {
        return res.end("unauthorized");
    }
    next();
});

app.post("/ytdl", (req, res) => {
    let id = req.body.id;
    if(!id || typeof id !== "string" || !/^[a-zA-Z0-9-_]{11}$/.test(id)) {
        return res.end();
    }
    let url = "https://www.youtube.com/watch?v=" + id;

    if(prev === url && prevData) {
        return res.end(prevData);
    }
    prev = url;

    try {
        let stream = ytdl(prev, { filter: 'audioonly' });
        let bufs = [];

        stream.on('data', (c) => bufs.push(c));
        stream.once('end', () => {
            prevData = Buffer.concat(bufs);
            return res.end(prevData);
        });
    }
    catch(err) {
        return res.end();
    }
});

app.post("/check", (req, res) => {
    let url = req.body.url;
    if(!url || typeof url !== "string" || !url.startsWith("http")) {
        return res.end("invalid url!");
    }
    exec(`curl -s --head --request GET "${url.replace(/"/g, '')}"`, {timeout: 1000}, (error, stdout, stderr) => {
        if(error || stderr || (!stdout.includes("200") && !stdout.includes("301"))) {
            return res.end(`the website is down!`);
        }
        return res.end(`the website is up!`);
    });
});

app.get("/", (req, res) => {
    return res.end("FlagBot API Server");
});

app.listen(PORT, () => {
    console.log(`FlagBot API Server listening on port ${PORT}`)
});
