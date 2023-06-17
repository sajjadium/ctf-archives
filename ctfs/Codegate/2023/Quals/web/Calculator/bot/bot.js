const fs = require("fs");
const net = require("net");
const puppeteer = require("puppeteer");

const sleep = time => new Promise(resolve => setTimeout(resolve, time))

const flag = fs.readFileSync("/flag.txt").toString();

async function visit(browser, url) {
    console.log("url : ", url);
    if (!url || !url.startsWith("http://") && !url.startsWith("https://")) {
        console.log("invalid url");
        return;
    }
    const context = await browser.createIncognitoBrowserContext();
    const page = await context.newPage();

    await page.goto("http://web/login.php");
    await page.type("#username", "guest");
    await page.type("#password", "guest");
    await page.click('#submitBtn');
    await sleep(1000);

    page.setCookie({
        "name": "FLAG",
        "value": flag,
        "domain": "web",
        "path": "/",
        "httpOnly": false,
        "sameSite": "Strict"
    })

    try {
        await page.goto(url);
        await sleep(10000);
    } catch (e) {
        console.log(e);
    }
    await context.close();
}

async function start() {
    let browser;
    try {
        browser = await puppeteer.launch({ args: ["--no-sandbox","--headless"] });

        const server = net.createServer();
        server.listen(5000);

        server.on("connection", (socket) => {
            socket.on("data", async (data) => {
                try {
                    if (socket.state == "waiting") {
                        socket.state = "running";
                        socket.write("running bot");
                        socket.end();
                        socket.destroy();

                        await visit(browser, data.toString());
                    }
                } catch (err) {
                    console.log(err);
                }
            });
            socket.state = "waiting";
        });
    } catch (err) {
        console.log(err);
        if (browser) {
            await browser.close();
        }
    }
}

start();