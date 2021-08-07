const express = require("express");

let app = express();
app.listen(3000, () => {
    console.log("Arithmetic app up on 3000");
});

app.get('/add', (req, res) => {
    if (!(req.query.n1 && req.query.n2)) {
        res.json({"error": "No number provided"});
    }
    res.json({"result": req.query.n1 + req.query.n2});
});

app.get('/sub', (req, res) => {
    if (!(req.query.n1 && req.query.n2)) {
        res.json({"error": "No number provided"});
    }
    res.json({"result": req.query.n1 - req.query.n2});
});

app.get('/div', (req, res) => {
    if (!(req.query.n1 && req.query.n2)) {
        res.json({"error": "No number provided"});
    }
    res.json({"result": req.query.n1 / req.query.n2});
});

app.get('/mul', (req, res) => {
    if (!(req.query.n1 && req.query.n2)) {
        res.json({"error": "No number provided"});
    }
    res.json({"result": req.query.n1 * req.query.n2});
});
