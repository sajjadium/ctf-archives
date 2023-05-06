import initExpress, { json, Response, static as serveStatic } from "express";
import dataTypeMiddleware, { loginType } from "./datatypemiddleware";
import { createHash } from "crypto";
import { Database } from "sqlite3";
import { randomBytes } from "crypto";
import menu from "./menu";
import { readFileSync } from "fs";
import cookieParser from "cookie-parser";

const flag = readFileSync("./flag.txt", "utf8");

const databases = new Map<string, Database>();

const authTokens = new Map<string, string>();

const server = initExpress();


const idTimeoutMillis = 10 * 60 * 1000;
const newDatabase = async (): Promise<string> => {
    let id: string;
    do {
        id = randomBytes(32).toString('base64');
    } while (databases.has(id));

    const db = new Database(`:memory:`);

    await Promise.all([
        new Promise(
            (res, rej) => db.exec(
                "CREATE TABLE users (username TEXT, password TEXT);",
                (err) => err ? rej(err) : res(undefined)
            )
        ),
        new Promise(
            (res, rej) => db.exec(
                "CREATE TABLE failed_logins (username TEXT, password TEXT);",
                (err) => err ? rej(err) : res(undefined)
            )
        ),
    ]);

    databases.set(id, db);

    console.log(`Successfully created database for id \`${id}\``);

    setTimeout(async () => {

        try {
            await new Promise((rej, res) => db.close(e => e ? rej(e) : res(undefined)));
            databases.delete(id);
            console.log(`Successfully killed database for id \`${id}\``);
        } catch (e) {
            console.error(e);
            console.log(`Failed while killing database for id \`${id}\``);
        }
    }, idTimeoutMillis);

    return id;
};

const reportError = (res: Response, err: any) => {
    const messages = [
        '*angry whooshing noises*',
        'The Bloodthirty Breeze is disappointed at your inability to not cause an error.',
    ];
    console.error(err);
    res.status(500);
    res.send(messages[Math.floor(Math.random() * messages.length)]);
}

server.post("/api/login", cookieParser(), json(), dataTypeMiddleware(loginType), async (req, res) => {
    try {
        let id = req.cookies.id;
        if (!databases.has(id)) {
            id = await newDatabase();
            res.cookie("id", id, {
                expires: new Date(new Date().getTime() + idTimeoutMillis),
            });
        }

        const db = databases.get(id);
        if (!db) {
            res.cookie("id", undefined);
            throw new TypeError(`Failed to find DB in databases database at id \`${id}\`!`);
        }

        const body: loginType = req.body;
        const {username, password} = body;

        const hashedPassword = (() => {
            const hash = createHash('md5');
            hash.update(password);
            return hash.digest().toString('base64');
        })();

        // Try to log in as the user
        const users = await new Promise<unknown[]>((resolve, reject) => {
            db.all(`SELECT * FROM users WHERE username = ? AND password = '${hashedPassword}';`, [username], (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });

        if (users.length > 0) {
            // Login succeeded, generate an auth token, set the cookie, and return a response
            const token = randomBytes(32).toString('base64');
            authTokens.set(token, username);
            res.cookie('auth', token);
            res.send("Log in successful! You are now authorized to access the menu.");
        } else {
            // Login failed, add the failed login to the database for auditing purposes
            await new Promise<void>((resolve, reject) => {
                db.exec(`INSERT INTO failed_logins VALUES ('${username}', '${hashedPassword}');`, err => {
                    if (err) {
                        reject(err);
                    } else {
                        resolve();
                    }
                });
            });
            res.status(403);
            res.send("Incorrect username or password.");
        }
    } catch (e) {
        reportError(res, e);
    }
});

server.get("/api/menu", cookieParser(), async (req, res) => {
    try {
        if (!databases.has(req.cookies.id)) res.cookie("id", await newDatabase(), {
            expires: new Date(new Date().getTime() + idTimeoutMillis),
        });

        if (!req.cookies.auth) {
            res.status(401);
            res.send(
                'The Bloodthirsty Breeze is interested in devouring your user data. Therefore, The Bloodthirsty Breeze requires that all visitors log in to view the menu, to maximize data collection efficiency.');
            return;
        }

        const authToken = req.cookies.auth;
        if (authTokens.has(authToken)) {
            const randIndex = Math.floor(Math.random() * menu.length);
            const result = menu.map((item, i) => ({ ...item, description: i === randIndex ? flag : item.description }));
            res.json(result);
        } else {
            res.status(401);
            res.send("Hacking The Bloodthirsty Breeze isn't a breeze, you know. Try harder.");
        }
    } catch (e) {
        reportError(res, e);
    }
});

server.use(serveStatic("./build"));

server.listen(3000);