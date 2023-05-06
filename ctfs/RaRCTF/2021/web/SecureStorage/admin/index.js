const express = require("express");
const app = express();

require("dotenv").config();

const PORT = process.env.PORT ? parseInt(process.env.PORT) : 80;

const admin = require("./admin.js");

app.use(express.urlencoded({ extended: false }));
app.use(express.json());

app.post("/xss/add", (req, res) => {
    if(!req.headers.authorization || req.headers.authorization !== process.env.XSSBOT_SECRET) {
        return res.end("unauthorized");
    }

    let { url } = req.body;
    if(!url) {
        return res.end("missing url");
    }
    admin.addToQueue(url);
    return res.end("done");
});

app.listen(PORT, () => {
    console.log(`xssbot listening on port ${PORT}`);
});