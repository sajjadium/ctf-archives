const fs = require("fs");
const net = require("net");
const puppeteer = require("puppeteer");

const flag = fs.readFileSync("/flag.txt").toString();

async function visit(url) {
    const browser = await puppeteer.launch({
        headless: "new",
        args: [
            '--disable-gpu',
            '--no-sandbox'
        ],
        executablePath: '/usr/bin/google-chrome'
    })
    try {
        let page = await browser.newPage();

        await page.goto("http://webserver/login.php");
        await page.waitForSelector('body')
        await page.focus('#username')

        await page.keyboard.type("admin", { delay: 10 });

        await page.focus('#password')
        await page.keyboard.type("[REDACTED]", { delay: 10 });
        
        await new Promise(resolve => setTimeout(resolve, 500))
        await page.click('#submitBtn')
        await new Promise(resolve => setTimeout(resolve, 500))

        page.setCookie({
            "name": "FLAG",
            "value": flag,
            "domain": "webserver",
            "path": "/",
            "httpOnly": false,
            "sameSite": "Strict"
        })

        console.log("url : ", url);
        await page.waitForNetworkIdle();
        await page.goto(url, {waitUntil: 'load'});
        await new Promise(resolve => setTimeout(resolve, 10000))
        await page.close()
        await browser.close()
    } catch (e) {
        console.log("error!",e);
        await browser.close()
    }
}

async function start() {
    try {
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

                        await visit(data.toString());
                    }
                } catch (err) {
                    console.log(err);
                }
            });
            socket.state = "waiting";
        });
    } catch (err) {
        console.log(err);
    }
}

start();