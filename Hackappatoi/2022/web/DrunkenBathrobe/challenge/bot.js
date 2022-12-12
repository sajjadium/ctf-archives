const puppeteer = require("puppeteer");

const browser_options = {
    executablePath: "/usr/bin/google-chrome", //-stable",
    headless: true,
    args: [
        "--no-sandbox",
        "--disable-background-networking",
        "--disable-default-apps",
        "--disable-extensions",
        "--disable-gpu",
        "--disable-sync",
        "--disable-translate",
        "--hide-scrollbars",
        "--metrics-recording-only",
        "--mute-audio",
        "--no-first-run",
        "--safebrowsing-disable-auto-update",
    ],
};

const cookies = [
    {
        name: "flag",
        value: process.env.FLAG,
    },
];

async function checkReport(query) {
    const browser = await puppeteer.launch(browser_options);
    try {
        const page = await browser.newPage();
        const urlToVisit = "http://127.0.0.1:1337/search?query=" + query;
        console.log("URL to visit:", urlToVisit);

        await page.goto("http://127.0.0.1:1337/");
        await page.setCookie(...cookies);

        await page.goto(urlToVisit, {
            waitUntil: "networkidle0",
            timeout: 10000,
        });

        await browser.close();
    } catch {
        await browser.close();
    }
}

// async function checkReport(url) {
//     const browser = await puppeteer.launch(browser_options);
//     const page = await browser.newPage();

//     await page.goto("http://127.0.0.1:1337/");
//     await page.setCookie(...cookies);

//     await page.goto(url, {
//         waitUntil: "networkidle2",
//     });

//     await browser.close();
// }
module.exports = { checkReport };
