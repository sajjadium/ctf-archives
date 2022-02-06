const express = require('express');
const fsp = require('fs/promises');
const crypto = require('crypto');

const { NodeVM } = require('vm2');
const vm = new NodeVM({
    eval: false,
    wasm: false,
    wrapper: 'none',
    strict: true
});

const PORT = process.env.PORT || 80;

const users = [
    { user: "strellic", pass: "4136805643780af20755baddcc947d20f7e38e52f421c3c89a5a8b9d8a8d1da7" },
    { user: "ginkoid", pass: "cdf72d24394745eab295c6e047ee41aaec62f56bd41e2cea4ef7d244d96b51dd" }
];

const sha256 = (data) => crypto.createHash('sha256').update(data).digest('hex');

const app = express();

app.set("view engine", "hbs");

app.use(express.urlencoded({ extended: false }));

app.get("/", (req, res) => res.render("index"));
app.post("/", (req, res) => {
    const { calc } = req.body;

    if(!calc) {
        return res.render("index");
    }

    let result;
    try {
        result = vm.run(`return ${calc}`);
    }
    catch(err) {
        console.log(err);
        return res.render("index", { result: "There was an error running your calculation!"});
    }

    if(typeof result !== "number") {
        return res.render("index", { result: "Nice try..."});
    }

    res.render("index", { result });
});

app.get("/admin", (req, res) => res.render("admin"));

app.post("/admin", async (req, res) => {
    let { user, pass } = req.body;
    if(!user || !pass || typeof user !== "string" || typeof pass !== "string") {
        return res.render("admin", { error: "Missing username or password!" });
    }

    let hash = sha256(pass);
    if(users.filter(u => u.user === user && u.pass === hash)[0] !== undefined) {
        res.render("admin", { flag: await fsp.readFile("flag.txt") });
    }
    else {
        res.render("admin", { error: "Incorrect username or password!" });
    }
});

app.listen(PORT, () => console.log(`vm-calc listening on port ${PORT}`));