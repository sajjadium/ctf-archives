const express = require("express");
const dnsp = require("dns/promises");
const isIpPrivate = require("private-ip");

const fetch = (...args) => import("node-fetch").then(({default: fetch}) => fetch(...args));

const app = express();

const PORT = process.env.PORT || 8080;

app.use(express.urlencoded({ extended: false }));
app.use(express.static("public"));

app.post("/preview", async (req, res) => {
    const { link } = req.body;
    if(!link || typeof link !== "string") {
        return res.send("Missing link");
    }

    let url;
    try {
        url = new URL(link);
    }
    catch(err) {
        return res.send("Invalid url");
    }

    if(!["http:", "https:"].includes(url.protocol)) {
        return res.send("Invalid url");
    }

    let dnsLookup;
    try {
        dnsLookup = await dnsp.lookup(url.hostname, 4);
    }
    catch(err) {
        return res.send("Could not resolve url");
    }

    console.log(dnsLookup);
    let { address } = dnsLookup;
    if(isIpPrivate(address)) {
        return res.send("You are not allowed to view this url");
    }

    try {
        let fetchReq = await fetch(link);
        fetchReq.body.pipe(res);
    }
    catch(err) {
        res.send("There was an error previewing your url");
    }
});

app.get("/flag", (req, res) => {
    console.log(req.socket.remoteAddress);
    if(req.socket.remoteAddress === "::ffff:127.0.0.1") {
        return res.send(process.env.FLAG || "flag{test_flag}");
    }
    res.send("No flag for you!");
});

app.listen(PORT, () => console.log(`app listening on port ${PORT}`));