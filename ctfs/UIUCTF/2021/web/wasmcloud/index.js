import express from "express";
import morgan from "morgan";
import bodyParser from "body-parser";
import hcaptcha from "hcaptcha";

import fs from "fs";
import { randomBytes } from "crypto"
import { spawn, execFile } from "child_process";

const app = express();
app.use(morgan("combined"));
app.use(express.static("static"));
app.use(bodyParser.raw({ limit: "10kb", type: "application/wasm" }));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(function (req, res, next) {
    res.header("Content-Type", "text/html");
    next();
});

app.get("/", (req, res, next) => {
    res.redirect("/app.html");
    next();
});

app.put("/upload", (req, res, next) => {
    // duck season
    const fn = randomBytes(8).toString("hex") + ".wasm";
    fs.writeFile("/files/" + fn, req.body, (err) => {
        if (err) {
            res.status(500);
            res.send(err);
        } else res.send(fn);
        next();
    });
});

// only allow one run at a time
const runQueue = [];
let running = false;

app.get("/run/:fn", (req, res, next) => {
    // wabt season
    const {fn} = req.params;
    if (!fn.match(/[0-9a-f]{16}\.wasm/)) return next();

    fs.readFile("/files/" + fn, async (err, data) => {
        if (err) {
            res.status(500);
            res.send(err);
            return next();
        }

        if (running) {
            await new Promise(resolve => {
                runQueue.push(resolve);
                console.log("Run queued", runQueue.length);
            });
        }
        running = true;

        res.writeHead(200);
        const proc = spawn("nsjail", [
            "-Mo", "-Q", "-N", "--disable_proc",
            "--chroot", "/chroot/",
            "--time_limit", "1",
            "--",
            "/usr/local/bin/node", "/sandbox.js"
        ]);
        proc.stdout.on("data", (data) => {
            res.write(data);
        });
        proc.stderr.on("data", (data) => {
            res.write(data);
        });
        proc.on("exit", (code) => {
            res.end("Exit code: " + code);
            if (runQueue.length) {
                runQueue.shift()();
            } else {
                running = false;
            }
            next();
        });
        proc.stdin.write(data);
        proc.stdin.end();
    });
});

app.post("/report", async (req, res, next) => {
    // assume url is to wasmcloud (client checks it, so there should be no confusion)
    const url = "http://127.0.0.1:1337" + new URL(req.body.url).pathname;

    // captcha
    if (process.env.HCAPTCHA_ENABLE !== "false" &&
        process.env.HCAPTCHA_BYPASS !== req.body.healthcheck_captcha_bypass) {
        const valid = (await hcaptcha.verify(process.env.HCAPTCHA_SECRET,
            req.body["h-captcha-response"])).success;
        if (!valid) {
            res.status(400);
            res.send("Invalid hCaptcha token");
            return next();
        }
    }

    // reply immediately
    res.send("Thanks for the URL. An admin will check it out shortly!");

    // run admin bot
    console.log("Admin bot:", url);
    spawn("node", ["bot.js", req.body.url]);
});

app.listen(1337);
