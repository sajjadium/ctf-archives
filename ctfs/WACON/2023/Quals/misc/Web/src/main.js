const express = require("express");
const bodyParser = require("body-parser");
const session = require("express-session");
const child_process  = require("child_process");

const crypto = require("crypto");
const random_bytes = size => crypto.randomBytes(size).toString();
const sha256 = plain => crypto.createHash("sha256").update(plain.toString()).digest("hex");

const users = new Map([
    [],
]);

const now = () => { return Math.floor(+new Date()/1000) }
const checkoutTimes = new Map()

const app = express();

app.use(bodyParser.json());
app.use(
    session({
        cookie: { maxAge : 600000 },
        secret: random_bytes(64),
    })
);

const loginHandler = (req, res, next) => {
    if(!req.session.uid) {
        return res.redirect("/")
    }
    next();
}

app.all("/", (req, res) => {
    return res.json({ "msg" : "hello guest" });
});

app.post("/login", (req, res) => {
    const { username, password } = req.body;

    if ( typeof username !== "string" || typeof password !== "string" || username.length < 4 || password.length < 6) {
        return res.json({ msg: "invalid data" });
    }

    if (users.has(username)) {
        if (users.get(username) === sha256(password)) {
            req.session.uid = username;

            return res.redirect("/");
        } else {
            return res.json({ msg: "Invalid Password" });
        }
    } else {
        users.set(username, sha256(password));
        req.session.uid = username;
        return res.redirect("/");
    }
});

app.post("/calc", loginHandler, (req,res) => {
	if(checkoutTimes.has(req.ip) && checkoutTimes.get(req.ip)+1 > now()) {
		return res.json({ error: true, msg: "too fast"})
	}
	checkoutTimes.set(req.ip,now())

    const { expr, opt } = req.body;
    const args = ["--experimental-permission", "--allow-fs-read=/app/*"];

    const badArg = ["--print", "-p", "--input-type", "--import", "-e", "--eval", "--allow-fs-write", "--allow-child-process", "-", "-C", "--conditions"]

    if (!expr || typeof expr !== "string" ) {
        return res.json({ msg: "invalid data" });
    }

    if (opt) {
        if (!/^--[A-Za-z|,|\/|\*|\=|\-]+$/.test(opt) || badArg.includes(opt.trim())) {
            return res.json({ error: true, msg: "Invalid option" });
        }
        args.push(opt, "eval.js", btoa(expr));
    }

    args.push("eval.js", btoa(expr));

	try {
		ps = child_process.spawnSync("node", args);
        result = ps.stdout.toString().trim();
        if (result) {
            return res.type("text/plain").send(result)
        } 
        return res.type("text/plain").send("Empty");
	} catch (e) {
        console.log(e)
        return res.json({ "msg": "Nop" })
    }
});

app.listen(80);