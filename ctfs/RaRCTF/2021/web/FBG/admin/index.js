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

    let length = admin.addToQueue(req.body);
    res.send({"position": length});
    return res.end();
});

app.listen(PORT, () => {
    console.log(`xssbot listening on port ${PORT}`);
});
