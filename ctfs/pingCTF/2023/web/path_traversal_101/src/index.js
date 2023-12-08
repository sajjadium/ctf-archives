import express from "express";
import { randomUUID } from "crypto";
import withCatch from "./withCatch.js";
import { task1, task2, task3, tasks } from "./tasks.js";
import cookieParser from "cookie-parser";

import rl from "./ratelimit.js";
import robot from "./robot.js";

const { FLAG } = process.env;

const app = express();
const port = 3000;

const sessions = [];

const createSession = () => {
    const id = randomUUID();
    return {
        id,
        task1: false,
        task2: false,
        task3: false,
    };
};

app.set("view engine", "ejs");
app.use(express.static("static"));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cookieParser());

app.get("/", (req, res) => {
    res.render("robot", {
        error: "",
    });
});

app.get("/robots.txt", (req, res) => {
    res.type("text/plain");
    res.send("User-agent: *\nDisallow: /🤖");
});

app.get("/%F0%9F%A4%96", robot, (req, res) => {
    const token = req.cookies.token;
    if (!token) {
        const session = createSession();
        sessions.push(session);
        res.cookie("token", session.id);
        res.render("exam", {
            task: tasks[0],
        });
    } else {
        const session = sessions.find((session) => session.id === token);
        if (!session) {
            const session = createSession();
            sessions.push(session);
            res.cookie("token", session.id);
            res.render("exam", {
                task: tasks[0],
            });
        } else {
            if (!session.task1) {
                res.render("exam", {
                    task: tasks[0],
                });
            } else if (!session.task2) {
                res.render("exam", {
                    task: tasks[1],
                });
            } else if (!session.task3) {
                res.render("exam", {
                    task: tasks[2],
                });
            } else {
                res.render("exam", {
                    task: FLAG,
                });
            }
        }
    }
});

app.get("/*", (req, res) => {
    res.render("robot", {
        error: "",
    });
});

app.post(
    "/%F0%9F%A4%96",
    rl,
    robot,
    withCatch(async (req, res) => {
        const token = req.cookies.token;
        if (!token) {
            throw new Error("Unauthorized");
        }
        const session = sessions.find((session) => session.id === token);
        if (!session) {
            throw new Error("Unauthorized");
        }
        const { solution } = req.body;
        if (!session.task1) {
            const result = task1(solution);
            if (result) {
                session.task1 = true;
                res.render("exam", {
                    task: tasks[1],
                });
            } else {
                res.render("exam", {
                    task: tasks[0],
                    error: "Try again!",
                });
            }
        } else if (!session.task2) {
            const result = task2(solution);
            if (result) {
                session.task2 = true;
                res.render("exam", {
                    task: tasks[2],
                });
            } else {
                res.render("exam", {
                    task: tasks[1],
                    error: "Try again!",
                });
            }
        } else if (!session.task3) {
            const result = task3(solution);
            if (result) {
                session.task3 = true;
                res.render("exam", {
                    task: FLAG,
                });
            } else {
                res.render("exam", {
                    task: tasks[2],
                    error: "Try again!",
                });
            }
        }
    })
);

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
