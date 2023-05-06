"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var ExpressSession = require("express-session");
var TextToImage = require("text-to-image");
var Express = require("express");
var Redis = require("ioredis");
var Fs = require("fs");
var app = Express();
var redis = new Redis(6379, "redis");
var total = [];
var time = Date.now();
var clear = function () {
    if (Date.now() - time > 60000) {
        time = Date.now();
        total = [];
    }
};
app.use(Express.urlencoded({ extended: true }));
app.use(Express.static(__dirname + "views"));
app.use(ExpressSession({
    secret: process.env.SECRET,
    saveUninitialized: false,
    resave: false,
    cookie: {
        maxAge: 60000
    }
}));
app.set("view engine", "ejs");
app.use(function (req, res, next) {
    res.set("Content-Security-Policy", "script-src 'unsafe-inline'");
    res.set("Content-Type", "text/html");
    clear();
    next();
});
app.get("/", function (req, res) {
    Fs.readdir("public", function (err, files) {
        var f = new Array();
        files.forEach(function (file) {
            f.push({
                t: file,
                s: Fs.statSync("public/".concat(file)).size
            });
        });
        res.render("index", { l: files.length, f: f });
    });
});
app.get("/insert", function (req, res) {
    res.render("insert");
});
app.post("/insert", function (req, res) {
    if (typeof req.body.title === "string" &&
        req.body.title.length < 30 &&
        typeof req.body.content === "string" &&
        req.body.content.length < 1024 * 256) {
        res.end("<script>document.cookie = 'FLAG=REMOVED'</script><h1>".concat(req.body.title, "</h1><hr/>") + req.body.content);
    }
    else {
        res.end("Something wrong with your book title or contents.");
    }
});
app.get("/:t/:s/:e", function (req, res) {
    var s = Number(req.params.s);
    var e = Number(req.params.e);
    var t = req.params.t;
    if ((/[\x00-\x1f]|\x7f|\<|\>/).test(t)) {
        res.end("Invalid character in book title.");
    }
    else {
        Fs.stat("public/".concat(t), function (err, stats) {
            if (err) {
                res.end("No such a book in bookself.");
            }
            else {
                if (s !== NaN && e !== NaN && s < e) {
                    if ((e - s) > (1024 * 256)) {
                        res.end("Too large to read.");
                    }
                    else {
                        Fs.open("public/".concat(t), "r", function (err, fd) {
                            if (err || typeof fd !== "number") {
                                res.end("Invalid argument.");
                            }
                            else {
                                var buf = Buffer.alloc(e - s);
                                Fs.read(fd, buf, 0, (e - s), s, function (err, bytesRead, buf) {
                                    res.end("<h1>".concat(t, "</h1><hr/>") + buf.toString("utf-8"));
                                });
                            }
                        });
                    }
                }
                else {
                    res.end("There isn't size of book.");
                }
            }
        });
    }
});
app.get("/report", function (req, res) {
    if (req.session.username) {
        var code = Math.random().toString(36).substr(2, 10);
        req.session.captcha = code;
        TextToImage.generate(code, {
            textAlign: "center",
            textColor: "#FFFFFF",
            bgColor: "#00B900",
            maxWidth: 300
        }).then(function (data) {
            res.render("report", { data: data });
        });
    }
    else {
        res.render("identify", { length: total.length });
    }
});
app.post("/report", function (req, res) {
    res.set("Content-Type", "application/json");
    if (!req.session.username) {
        res.json({
            error: true,
            message: "You are not identified."
        });
    }
    if (req.session.captcha != "" && req.body.captcha == req.session.captcha) {
        req.session.captcha = "";
        if (typeof req.body.url === "string" && req.body.url.startsWith("/") && req.body.url.length < 500) {
            redis.lpush("query", req.body.url);
            res.json({
                error: false,
                message: "Reported successfully."
            });
        }
        else {
            res.json({
                error: true,
                message: "Invalid url.",
            });
        }
    }
    else {
        res.json({
            error: true,
            message: "Invalid captcha."
        });
    }
});
app.post("/identify", function (req, res) {
    res.set("Content-Type", "application/json");
    if (!req.session.username) {
        if (typeof req.body.username === "string" && req.body.username.length < 100) {
            req.session.username = req.body.username;
            total.push(req.body.username);
            res.json({
                error: false,
                message: "Identified successfully."
            });
        }
        else {
            res.json({
                error: true,
                message: "Username is invalid or too long."
            });
        }
    }
    else {
        res.json({
            error: true,
            message: "You are already identified as " + req.session.username
        });
    }
});
app.listen(80, function () {
    console.log("> Express server is running on 80!");
});
//# sourceMappingURL=app.js.map