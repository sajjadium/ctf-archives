const crypto = require("crypto")
const express = require("express")
const session = require("express-session")
const otpauth = require("otpauth")
const bodyParser = require("body-parser")
const puppeteer = require("puppeteer")

const app = express();
const token = getTOTPSecretToken();

// ##################
// # Middleware
// ##################

app.use(express.static("public"))
app.use(bodyParser.json())
app.use(session({
    secret: crypto.randomBytes(32).toString("base64"),
    cookie: {
        httpOnly: true
    }
}))

// ##################
// # helper functions
// ##################


function getTOTPSecretToken() {
    var token = otpauth.Secret.fromHex(crypto.randomBytes(32).toString("hex"))
    return token;
}

function sleep(ms) {
    return new Promise(function(resolve, _) {
        setTimeout(_ => resolve(), ms);
    })
}

// ##################
// # local database
// ##################


const totp_tokens = {}
const secret_notes = {}

// ##################
// # Server logic
// ##################

app.post("/setup_2fa", (req, res) => {
    const sessionId = req.session.id;
    if(Object.keys(totp_tokens).includes(sessionId)) return res.status(400).send("TOTP already registered for that session!")
    const totp = new otpauth.TOTP({
        issuer: "GlacierTV",
        label: "2FA",
        algorithm: "SHA3-384",
        digits: 9,
        period: 43,
        secret: getTOTPSecretToken()
    });
    totp_tokens[sessionId] = totp
    res.json({
        "totp": totp.toString()
    })
});

app.post("/secret_note", (req, res) => {
    const sessionId = req.session.id;
    const message = req.body.message;
    if(typeof message !== "string") return res.status(400).send("No message given");
    secret_notes[sessionId] = message;
    res.status(204).end();
});

app.get("/secret_note", (req, res) => {
    const sessionId = req.session.id;
    if(Object.keys(totp_tokens).includes(sessionId)) {
        const token = req.query.token;
        if(typeof token !== "string") return res.status(400).send("Missing TOTP token in search query.")
        const delta = totp_tokens[sessionId].validate({token, window: 1})
        if(delta === null) return res.status(400).send("Invalid TOTP token!") 
    }
    res.json({
        message: secret_notes[sessionId]
    })
});

// ##################
// # Report engine
// ##################

const FLAG = process.env.FLAG || "gctf{dummy}";

app.post("/report", async (req, res) => {
    try {
        const path = req.body.path;
        if(typeof path !== "string") return res.status(400).send("No path provided");
        const uri = `http://localhost:8080/${path}`

        const browser = await puppeteer.launch({
            headless: "new",
            args: ["--no-sandbox", "--disable-dev-shm-usage", "--disable-setuid-sandbox"],
        });
        const context = await browser.createIncognitoBrowserContext();
        const page = await context.newPage();
        await page.goto('http://localhost:8080/');
        await page.waitForNavigation({
            waitUntil: 'networkidle0',
        });
        await page.evaluate(async message => {
            await fetch("/setup_2fa", {method: "POST"});
            await fetch("/secret_note", {
                method: "POST",
                body: JSON.stringify({message}),
                headers: {
                    "Content-Type": "application/json"
                }
            });
        }, FLAG)
        await page.goto(uri);
        await sleep(5000);
        await browser.close();
        res.status(200).send("Thank you for your report. We will check it soon")
    } catch(err) {
	    console.log(err)
        res.status(400).send("Something went wrong! If you think this is an error on our site, contact an admin.")
    }
})

app.listen(8080);
