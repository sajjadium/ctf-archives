import express from "express"
import crypto from "crypto"
import bodyParser from "body-parser"
import cookieParser from "cookie-parser"
import fetch from "node-fetch"
import dns from "dns"
import ipaddr from "ipaddr.js"
import { __trigger_browser_password_manager } from "./pwm.js"
import { startFlagserver } from "./flagserver.js"

startFlagserver();
const app = express();
const sha256 = data => crypto.createHash('sha256').update(data).digest('hex');
app.use(function(req, res, next) {
    console.log("[DEBUG] "+req.method+" "+req.url);
    if(req.body) console.log("[DEBUG] "+JSON.stringify(req.body));
    return next();
});
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());

const AUTH_TOKEN_REPORT = process.env.AUTH_TOKEN_REPORT || 'supersecret';
const REPORT_URL = process.env.REPORT_URL || 'http://headless:5000/'
const PASSWORD = process.env.PASSWORD || 'fake_password';

let front = (res, info)=>{
    let data = "";
    if(info) {
        data = `<div style="padding: 10px; border: 2px solid #FF5733; border-radius: 5px; background: transparent; color: #FF5733; text-align: center; font-size: 20px; display: block; margin-bottom: 10px; font-size: 24px;">${info}</div>`;
    }
    return res.send(`
<html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&amp;family=Inter:wght@300&amp;display=swap" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@300&display=swap" rel="stylesheet">
        <script>async function ccreport() {
            let url = prompt("URL to report:");
            if (url) fetch("/report", { method: "POST", body: new URLSearchParams({ url }), headers: { "Content-Type": "application/x-www-form-urlencoded" } }).then(response => response.text()).then(x => alert(x));
        }</script>
        <title>Super Admin Panel</title>
    </head>
    <body style="font-family: 'Inter'; max-width: 700px; margin: 0 auto; background-color: #08090f; padding: 20px; color: #0095ff;">
        <h1 style="font-size: 3rem; font-family: 'JetBrains Mono', monospace;">Super Admin Panel</h1>
        ${data}
        <form action="/panel" method="POST" style="background-color: rgba(0, 0, 0, 0.7); padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 255, 0.7);">
            <input id="username" name="username" type="text" placeholder="Username" style="width: 100%; padding: 10px; border: 2px solid #007BFF; border-radius: 5px; background: transparent; margin-bottom: 10px; display:block; color: #fff; font-size: 20px;">
            <input id="password" name="password" type="password" placeholder="Password" style="width: 100%; padding: 10px; border: 2px solid #007BFF; border-radius: 5px; background: transparent; margin-bottom: 10px; display:block; color: #fff; font-size: 20px;">
            <button style="width: 100%; padding: 10px; background-color: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer; display:block; color: #fff; font-size: 20px; margin-bottom: 10px;" type="submit" value="Submit">Login</button>
            <button id="pwn" style="width: 100%; padding: 10px; background-color: transparent; border: 2px solid #007BFF; color: white; border-radius: 5px; cursor: pointer; display:block; color: #fff; font-size: 20px;" type="button">&nbsp;</button>
        </form>
        <a href="#" onclick="ccreport()" style="font-size: 2rem; font-family: 'JetBrains Mono', monospace;">Report</a>
    </body>
</html>`)
};

let panel = (res, info)=>{
    let data = "";
    if(info) {
        data = `<div style="padding: 10px; border: 2px solid #FF5733; border-radius: 5px; background: transparent; color: #FF5733; text-align: center; font-size: 20px; display: block; margin-bottom: 10px; font-size: 24px;">${info}</div>`;
    }
    return res.send(`
<html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&amp;family=Inter:wght@300&amp;display=swap" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@300&display=swap" rel="stylesheet">
        <title>Super Admin Panel</title>
    </head>
    <body style="font-family: 'Inter'; max-width: 700px; margin: 0 auto; background-color: #08090f; padding: 20px; color: #0095ff;">
        <h1 style="font-size: 3rem; font-family: 'JetBrains Mono', monospace;">Super Admin Panel</h1>
        <h2 style="font-size: 2rem; font-family: 'JetBrains Mono', monospace;">Test website functionality</h2>
        <form action="/panel" method="POST" style="background-color: rgba(0, 0, 0, 0.7); padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 255, 0.7);">
            <input id="link" name="link" type="text" placeholder="Link" style="width: 100%; padding: 10px; border: 2px solid #007BFF; border-radius: 5px; background: transparent; margin-bottom: 10px; display:block; color: #fff; font-size: 20px;">
            <button style="width: 100%; padding: 10px; background-color: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer; display:block; color: #fff; font-size: 20px; margin-bottom: 10px;" type="submit" value="Submit">Go</button>
        </form>
        ${data}
    </body>
</html>`)
};

app.get('/', (req, res) => {
    return front(res);
})

app.post('/report', (req, res) => {
    if(!req.body.url) return res.send("No url");
    if(typeof req.body.url !== "string") return res.send("Invalid url");
    if(!req.body.url.startsWith("https://")&&!req.body.url.startsWith("http://")) return res.send("invalid url");
    fetch(REPORT_URL, {
        method: 'POST',
        body: JSON.stringify({
            actions: [
                {type: "request", url: req.body.url, method: "GET"},
                {type: "sleep", time: 2},
                {type: "click", element: "#pwn"},
                ...__trigger_browser_password_manager,
                {type: "click", element: "#pwn"}
            ],
            timeout: 10
        }),
        headers: {
            'Content-Type': 'application/json',
            "X-Auth": AUTH_TOKEN_REPORT
        }
    }).then((x)=>x.json()).then((x)=>{
        if(x.job) return res.send("Admin will visit");
        console.error(x)
        return res.send("Error");
    }).catch((e)=>{
        console.error(e);
        return res.send("Error");
    })
});

function checkVCred(w){
    if(!w) return true;
    return sha256(w) !== sha256(PASSWORD);
}
app.use("/panel", (req, res, next) => {
    if(!req.cookies.passw || checkVCred(req.cookies.passw)){
        if((!req.body.username || !req.body.password) && (req.query.username && req.query.password)) {
            req.body = {
                username: req.body.username,
                password: req.body.password
            }
        }
        if(!req.body.username || !req.body.password) {
            return front(res, "No username or pw");
        }
        if(typeof req.body.username !== "string" || typeof req.body.password !== "string"){
            return front(res, "Stay away hacker!");
        }
        if(checkVCred(Buffer.from(req.body.password, 'base64').toString('utf8'))){
            return front(res, `Wrong password: ${Buffer.from(req.body.password, 'base64')}`);
        }
        return res.cookie("passw", Buffer.from(req.body.password, 'base64').toString('utf8'), { maxAge: 900000, httpOnly: true }).redirect("/panel");
    } else {
        return next();
    }
})
app.get("/panel", (req, res) => {
    return panel(res);
});
app.post("/panel", async (req, res) => {
    if(!req.body.link) {
        return panel(res);
    }
    try {
        let x = new URL(req.body.link);
        if(x.hostname === "localhost") throw "Invalid IP";
        let ip = await dns.promises.resolve(x.hostname);
        if(ipaddr.parse(ip[0]).range() === "private") throw "Invalid IP";
        return panel(res, `Content: ${await (await fetch(req.body.link, {
            timeout: 2000
        })).text()}`);
    } catch (e) {
        console.log(e);
        return panel(res, "Hackers not allowed");
    }
});

app.listen(80, '0.0.0.0', () => {
  console.log(`Adminpanel on :${process.env.CHALL_PORT || 777}`)
})