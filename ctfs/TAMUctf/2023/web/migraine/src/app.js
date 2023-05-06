const path = require('path');
const express = require("express");
const app = express();
const port = 8000;

app.use(express.json());

process.on('uncaughtException', (err, origin) => {
    console.log(err);
});

app.get("/", function (req, res) {
    res.sendFile(path.join(__dirname+'/static/index.html'));
});

app.post("/", function (req, res) {
    var src = req.body['src'];

    if (src.match(/[A-Za-z0-9]/) != null) {
        res.status(418).end('Bad character detected.');
        return;
    }

    try {
        eval(src);
    } catch(err) {
        res.status(418).end('Error on eval.');
        return;
    }

    res.status(200).send('Success!');
    return;
});

app.listen(port, function () {
    console.log(`Example app listening on port ${port}!`);
});
