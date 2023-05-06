import * as ExpressSession from "express-session";
import * as TextToImage from "text-to-image";
import * as Express from "express";
import * as Redis from "ioredis";
import * as Fs from "fs";

declare module "express-session" {
    export interface SessionData {
        username: string,
        captcha: string
    }
}

const app: Express.Application = Express();
const redis: any = new Redis(6379, "redis");
let total: Array<string> = [];
let time: number = Date.now();

const clear: Function = (): void => {
    if (Date.now() - time > 120000) {
        time = Date.now()
        total = []
    }
}

app.use(Express.urlencoded({ extended: true }))
app.use(Express.static(__dirname + "views"));
app.use(
    ExpressSession({
        secret: process.env.SECRET,
        saveUninitialized: false,
        resave: false,
        cookie: {
            maxAge: 60000
        }
    })
);
app.set("view engine", "ejs");

app.use((req: Express.Request, res: Express.Response, next: Express.NextFunction): void => {
    res.set("Content-Security-Policy", "script-src 'unsafe-inline'");
    res.set("Content-Type", "text/html")
    clear()
    next()
});

app.get("/", (req: Express.Request, res: Express.Response): void => {
    Fs.readdir("public", (err: NodeJS.ErrnoException, files: string[]): void => {
        let f = new Array()
        files.forEach((file: string): void => {
            f.push({
                t: file,
                s: Fs.statSync(`public/${file}`).size
            })
        })
        res.render("index", { l: files.length, f: f })
    })
});

app.get("/insert", (req: Express.Request, res: Express.Response): void => {
    res.render("insert")
});

app.post("/insert", (req: Express.Request, res: Express.Response): void => {
    if (
        typeof req.body.title === "string" &&
        req.body.title.length < 30 &&
        typeof req.body.content === "string" &&
        req.body.content.length < 1024 * 256
    ) {
        res.end(`<script>document.cookie = 'FLAG=REMOVED'</script><h1>${req.body.title}</h1><hr/>` + req.body.content);
    } else {
        res.end("Something wrong with your book title or contents.");
    }
});

app.get("/:t/:s/:e", (req: Express.Request, res: Express.Response): void => {
    const s: number = Number(req.params.s)
    const e: number = Number(req.params.e)
    const t: string = req.params.t

    if ((/[\x00-\x1f]|\x7f|\<|\>/).test(t)) {
        res.end("Invalid character in book title.")
    } else  {
        Fs.stat(`public/${t}`, (err: NodeJS.ErrnoException, stats: Fs.Stats): void => {
            if (err) {
                res.end("No such a book in bookself.")
            } else {
                if (s !== NaN && e !== NaN && s < e) {
                    if ((e - s) > (1024 * 256)) {
                        res.end("Too large to read.")
                    } else {
                        Fs.open(`public/${t}`, "r", (err: NodeJS.ErrnoException, fd: any): void => {
                            if (err || typeof fd !== "number") {
                                res.end("Invalid argument.")
                            } else {
                                let buf: Buffer = Buffer.alloc(e - s);
                                Fs.read(fd, buf, 0, (e - s), s, (err: NodeJS.ErrnoException, bytesRead: number, buf: Buffer): void => {
                                    res.end(`<h1>${t}</h1><hr/>` + buf.toString("utf-8"))
                                })
                            }
                        })
                    }
                } else {
                    res.end("There isn't size of book.")
                }
            }
        })
    }
});

app.get("/report", (req: Express.Request, res: Express.Response): void => {
    if (req.session.username) {
        const code: string = Math.random().toString(36).substr(2, 10)
        req.session.captcha = code
        TextToImage.generate(code, {
            textAlign: "center",
            textColor: "#FFFFFF",
            bgColor: "#00B900",
            maxWidth: 300
        }).then((data) => {
            res.render("report", { data })
        });
    } else {
        res.render("identify", { length: total.length })
    }
});

app.post("/report", (req: Express.Request, res: Express.Response): void => {
    res.set("Content-Type", "application/json")
    if (!req.session.username) {
        res.json({
            error: true,
            message: "You are not identified."
        })
    }
    if (req.session.captcha != "" && req.body.captcha == req.session.captcha) {
        req.session.captcha = ""
        if (typeof req.body.url === "string" && req.body.url.startsWith("/") && req.body.url.length < 500) {
            redis.lpush("query", req.body.url)
            res.json({
                error: false,
                message: "Reported successfully."
            })
        } else {
            res.json({
                error: true,
                message: "Invalid url.",
            })
        }
    } else {
        res.json({
            error: true,
            message: "Invalid captcha."
        })
    }
});

app.post("/identify", (req: Express.Request, res: Express.Response): void => {
    res.set("Content-Type", "application/json");
    if (!req.session.username) {
        if (typeof req.body.username === "string" && req.body.username.length < 100) {
            req.session.username = req.body.username
            total.push(req.body.username)
            res.json({
                error: false,
                message: "Identified successfully."
            })
        } else {
            res.json({
                error: true,
                message: "Username is invalid or too long."
            })
        }
    } else {
        res.json({
            error: true,
            message: "You are already identified as " + req.session.username
        })
    }
});

app.listen(80, (): void => {
    console.log("> Express server is running on 80!")
});