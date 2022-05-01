import express from "express";
import fetch from "node-fetch";
import path from "path";
import { fileURLToPath, URL } from "url";
import { resolve4 } from "dns/promises";

function isIpv4(str) {
    const chunks = str.split(".").map(x => parseInt(x, 10));
    return chunks.length === 4 && chunks.every(x => !isNaN(x) && x >= 0 && x < 256);
}

function isPublicIp(ip) {
    const chunks = ip.split(".").map(x => parseInt(x, 10));
    if ([127, 0, 10, 192].includes(chunks[0])) {
        return false;
    }
    if (chunks[0] == 172 && chunks[1] >= 16 && chunks[1] < 32) {
        return false;
    }
    return true;
}

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const app = express();
app.use(express.urlencoded({ extended: false }));

// environment config
const port = Number(process.env.PORT) || 8080;
const flag =
    process.env.FLAG ||
    "actf{someone_is_going_to_submit_this_out_of_desperation}";

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "index.html"));
});

app.post("/proxy", async (req, res) => {
    try {
        const url = new URL(req.body.url);
        const originalHost = url.host;
        if (!isIpv4(url.hostname)) {
            const ips = await resolve4(url.hostname);
            // no dns rebinding today >:)
            url.hostname = ips[0];
        }
        if (!isPublicIp(url.hostname)) {
            res.type("text/html").send("<p>private ip contents redacted</p>");
        } else {
            const abort = new AbortController();
            setTimeout(() => abort.abort(), 3000);
            const resp = await fetch(url.toString(), {
                method: "POST",
                body: "ping=pong",
                headers: {
                    Host: originalHost,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                signal: abort.signal,
            });
            res.type("text/html").send(await resp.text());
        }
    } catch (err) {
        res.status(400).type("text/plain").send("got error: " + err.message);
    }
});

// make flag accessible for local debugging purposes only
// also the nginx is at a private ip that isn't 127.0.0.1
// it's not that easy to get the flag :D
app.post("/flag", (req, res) => {
    if (!["127.0.0.1", "::ffff:127.0.0.1"].includes(req.socket.remoteAddress)) {
        res.status(400).type("text/plain").send("You don't get the flag!");
    } else {
        res.type("text/plain").send(flag);
    }
});

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
