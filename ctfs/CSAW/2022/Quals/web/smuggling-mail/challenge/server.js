const { spawn } = require("child_process");
const path = require("path");

const express = require("express");
const kill = require("tree-kill");

const app = express();
const port = 8082;
const timeout = 10000;

app.use(express.json());
app.use(express.urlencoded());

app.use("/", express.static(path.join(__dirname, "public")));
app.use("/admin", express.static(path.join(__dirname, "admin")));

app.post("/waitlist", (req, res) => {
    res.send("Sorry, the waitlist is currently closed.");
});

// Emergency alert email notification system for all residents
app.post("/admin/alert", (req, res) => {
    if (req.body.msg) {
        const proc = spawn("mail", ["-s", "ALERT", "all_residents@localhost"], {timeout});
        proc.stdin.write(req.body.msg);
        proc.stdin.end();
        setTimeout(() => { kill(proc.pid); }, timeout);
    }

    res.end();
});

app.listen(port);
