const express = require("express");
const isEven = require("is-even");
const isOdd = require("is-odd");
const isNumber = require("is-number");

let app = express();
app.listen(3000, () => {
    console.log("Checker app up on 3000");
});

app.get('/is_even', (req, res) => {
    if (!req.query.n) {
        res.json({"error": "No number provided"});
    }
    res.json({"result":isEven(req.query.n)});
});

app.get('/is_odd', (req, res) => {
    if (!req.query.n) {
        res.json({"error": "No number provided"});
    }
    res.json({"result":isOdd(req.query.n)});
});

app.get('/is_number', (req, res) => {
    if (!req.query.n) {
        res.json({"error": "No number provided"});
    }
    res.json({"result":isNumber(req.query.n)});
});
