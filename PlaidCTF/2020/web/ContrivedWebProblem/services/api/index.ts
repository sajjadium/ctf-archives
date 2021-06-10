import express from "express";
import { Provider } from "nconf";
import { Pool, PoolClient } from "pg";
import * as bodyParser from "body-parser";
import bcrypt from "bcrypt";
import Ftp from "ftp";
import amqp from "amqplib";
import cookieParser from "cookie-parser";
import fetch from "isomorphic-fetch";

type UserAuth = {
    id: string;
    name: string;
    profile?: string | null;
    email: string;
}

declare global {
    namespace Express {
        export interface Request {
            auth: undefined | UserAuth;
        }
    }
}

const nconf = (new Provider())
    .argv()
    .env()
    .defaults({
        "P_PSQL_USER": "postgres",
        "P_PSQL_PASS": undefined,
        "P_PSQL_HOST": "localhost",
        "P_PSQL_PORT": "5432",
        "P_FTP_HOST": "localhost",
        "P_FTP_PORT": "2121",
        "P_RABBIT_USER": "test",
        "P_RABBIT_PASS": "test",
        "P_RABBIT_HOST": "localhost",
        "P_RABBIT_PORT": "5672",
    })

const streamToBuffer = (stream: NodeJS.ReadableStream): Promise<Buffer> => {
    return new Promise((resolve, reject) => {
        let result = Buffer.from([]);
        stream.on("data", (data) => {
            result = Buffer.concat([result, Buffer.from(data)]);
        });
        stream.on("end", () => resolve(result));
    });
}

const isPNG = (imageBuffer: Buffer) =>
    (imageBuffer[0] === 0x89 && imageBuffer[1] === 0x50 && imageBuffer[2] === 0x4E && imageBuffer[3] === 0x47);

const connectFtp = async (args: Ftp.Options) => {
    let ftpInst = await new Promise<Ftp>((resolve, reject) => {
        const client = new Ftp();
        client.on("ready", () => resolve(client));
        client.on("error", (e) => reject(e));
        client.connect(args);
    });

    return {
        get: (path: string) =>
            new Promise<Buffer>((resolve, reject) =>
                ftpInst.get(path, (err, data) =>
                    err ? reject(err) : resolve(streamToBuffer(data)))),
        put: (path: string, data: Buffer) =>
            new Promise<void>((resolve, reject) =>
                ftpInst.put(data, path, (err) => err ? reject(err) : resolve())),
        mkdir: (path: string) =>
            new Promise<void>((resolve, reject) =>
                ftpInst.mkdir(path, true, (err) => err ? reject(err) : resolve())),
    };
}

const main = async () => {
    const rabbit = await amqp.connect({
        hostname: nconf.get("P_RABBIT_HOST"),
        port: nconf.get("P_RABBIT_PORT"),
        username: nconf.get("P_RABBIT_USER"),
        password: nconf.get("P_RABBIT_PASS"),
    });

    const pool = new Pool({
        host: nconf.get("P_PSQL_HOST"),
        user: nconf.get("P_PSQL_USER"),
        password: nconf.get("P_PSQL_PASS"),
        port: nconf.get("P_PSQL_PORT"),
        max: 20,
    });

    const withClient = <T>(fn: (client: PoolClient) => T | Promise<T>): Promise<T> =>
        new Promise((resolve, reject) =>
            pool.connect(async (err, client, release) => {
                try {
                    resolve(await fn(client))
                } catch (e) {
                    reject(e);
                } finally {
                    release()
                }
            })
        );

    const app = express();

    app.use("/", cookieParser());
    app.use("/", bodyParser.json({ limit: "1mb" }));
    app.use("/", async (req, res, next) => {
        let authCookie = req.cookies["authentication"];
        if (authCookie !== undefined) {
            let userResults = await withClient((client) =>
                client.query(`
SELECT user_auth.*
FROM user_auth
INNER JOIN user_token
    ON user_auth.id = user_token.user_id
WHERE user_token.token = $1
LIMIT 1
                `, [authCookie])
            );

            if (userResults.rowCount !== 1) {
                req.auth = undefined;
            } else {
                let user = userResults.rows[0]
                req.auth = {
                    id: user.id,
                    name: user.name,
                    email: user.email,
                    profile: user.profile,
                };
            }
        } else {
            req.auth = undefined;
        }

        next();
    });

    app.post("/register", async (req, res) => {
        let { name, email, password } = req.body;
        if (typeof name !== "string" || typeof email !== "string" || typeof password !== "string") {
            return res.status(500).send("Bad body");
        }

        let existingUser = await withClient((client) => client.query(`SELECT * FROM user_auth WHERE email = $1`, [email]));
        if (existingUser.rowCount >= 1) {
            return res.status(500).send("User already exists");
        }

        let hashedPassword = await bcrypt.hash(password, 14);
        let { rows: [ { id } ] } = await withClient((client) => client.query(`
INSERT INTO user_auth (name, email, password)
VALUES ($1, $2, $3)
RETURNING id
        `, [name, email, hashedPassword]));

        let { rows: [ { token } ] } = await withClient((client) => client.query(`
INSERT INTO user_token (user_id)
VALUES ($1)
RETURNING token
        `, [id]));

        res.cookie("authentication", token);
        res.status(200).send("Registered");
    });

    app.post("/login", async (req, res) => {
        let { email, password } = req.body;
        if (typeof email !== "string" || typeof password !== "string") {
            return res.status(500).send("Bad body");
        }

        let userQuery = await withClient((client) => client.query(`SELECT * FROM user_auth WHERE email = $1`, [email]));
        if (userQuery.rowCount < 1) {
            return res.status(500).send("Bad credentials");
        }

        let user = userQuery.rows[0];
        let passwordValid = await bcrypt.compare(password, user.password);
        if (!passwordValid) {
            return res.status(500).send("Bad credentials");
        }

        let { rows: [{ token }] } = await withClient((client) => client.query(`
INSERT INTO user_token (user_id)
VALUES ($1)
RETURNING token
        `, [user.id]));

        res.cookie("authentication", token);
        res.status(200).send("Logged in");
    });

    app.post("/password-reset", async (req, res) => {
        let { email } = req.body;

        if (typeof email !== "string") {
            res.status(500).send("Bad body");
        }

        let newPassword = Array.from(new Array(16), () => "abcdefghijklmnopqrstuvwxyz0123456789"[Math.floor(Math.random() * 36)]).join("");
        let hashedPassword = await bcrypt.hash(newPassword, 14);
        await withClient((client) => client.query(`
UPDATE user_auth
SET password = $2
WHERE email = $1
        `, [email, hashedPassword]));

        let channel = await rabbit.createChannel();
        channel.sendToQueue("email", Buffer.from(JSON.stringify({
            to: email,
            subject: "Password Reset",
            text: `Hello there, your new password is ${newPassword}`,
        })));

        res.status(200).send("Password reset");
    });

    app.get("/self", async (req, res) => {
        if (req.auth === undefined) {
            return res.status(500).send("Not logged in");
        }

        res.status(200).send(({
            name: req.auth.name,
            email: req.auth.email,
            profile: req.auth.profile,
        }));
    });

    app.post("/profile", async (req, res) => {
        if (req.auth === undefined) {
            return res.status(500).send("Not logged in");
        }
        if (req.body.url && typeof req.body.url === "string") {
            await withClient((client) => client.query(`
UPDATE user_auth
SET profile = $2
WHERE id = $1
            `, [req.auth!.id, req.body.url]));

            return res.status(200).send("Updated");
        } else if (req.body.image && typeof req.body.image === "string") {
            let imageBuffer = Buffer.from(req.body.image, "base64");
            if (imageBuffer.length > 512 * 1024) {
                return res.status(500).send("Image too large (> 0.5 megs)");
            }

            if (!isPNG(imageBuffer)) {
                return res.status(500).send("Image must be a PNG");
            }

            let client = await connectFtp({
                host: nconf.get("P_FTP_HOST"),
                port: nconf.get("P_FTP_PORT"),
            });

            await client.mkdir(`/user/${req.auth.id}/`);
            let url = `/user/${req.auth.id}/profile.png`
            await client.put(url, imageBuffer);

            let ftpUri = `ftp://${nconf.get("P_FTP_HOST")}:${nconf.get("P_FTP_PORT")}${url}`;

            await withClient((client) => client.query(`
UPDATE user_auth
SET profile = $2
WHERE id = $1
            `, [req.auth!.id, ftpUri]));

            res.status(200).send("Profile updated");
        }
    });

    app.post("/post", async (req, res) => {
        if (req.auth === undefined) {
            return res.status(500).send("Not logged in");
        }

        let { message } = req.body;

        if (typeof message !== "string") {
            return res.status(500).send("Bad body");
        }

        await withClient((client) => client.query(`
INSERT INTO posts (user_id, message, message_time)
VALUES ($1, $2, $3)
        `, [req.auth!.id, message, new Date()]));

        res.status(200).send("Saved message");
    });

    app.get("/posts", async (req, res) => {
        if (req.auth === undefined) {
            return res.status(500).send("Not logged in");
        }

        let posts = await withClient((client) => client.query(`
SELECT * FROM posts
WHERE user_id = $1
        `, [req.auth!.id]));

        res.status(200).send(posts.rows.map(({ message, message_time}) => ({ message, messageTime: message_time})));
    })

    app.get("/image", async (req, res) => {
        let { url } = req.query;
        if (typeof url !== "string") {
            return res.status(500).send("Bad body");
        }

        let parsed = new URL(url);

        let image: Buffer;
        if (parsed.protocol === "http:" || parsed.protocol === "https:") {
            const imageReq = await fetch(parsed.toString(), { method: "GET" });
            image = await (imageReq as any).buffer();
        } else if (parsed.protocol === "ftp:") {
            let username = decodeURIComponent(parsed.username);
            let password = decodeURIComponent(parsed.password);
            let filename = decodeURIComponent(parsed.pathname);
            let ftpClient = await connectFtp({
                host: parsed.hostname,
                port: parsed.port !== "" ? parseInt(parsed.port) : undefined,
                user: username !== "" ? username : undefined,
                password: password !== "" ? password : undefined,
            });
            image = await ftpClient.get(filename);
        } else {
            return res.status(500).send("Bad image url");
        }

        if (!isPNG(image)) {
            return res.status(500).send("Bad image (not a png)");
        }

        res.type(".png").status(200).send(image);
    })

    app.listen("4101");
}

main();