import * as Puppeteer from "puppeteer";
import Redis from "ioredis";

const redis: Redis = new Redis(6379, "redis");

(async (): Promise<void> => {
    while (true) {
        try {
            const [error, data]: any = await redis.blpop("query", 0);
            if (data) {
                console.log("> Start to process - http://web:8000" + data);
                await (async (url: string): Promise<void> => {
                    const bot: Puppeteer.Browser = await Puppeteer.launch({
                        executablePath: "/usr/bin/chromium",
                        product: "chrome",
                        headless: false,
                        ignoreHTTPSErrors: true,
                        args: [
                            "--no-sandbox",
                            "--load-extension=/bot/extension",
                            "--disable-extensions-except=/bot/extension",
                            "--enable-automation",
                        ],
                    });
                    const page: Puppeteer.Page = await bot.newPage();
                    await page.setCookie({
                        domain: "web",
                        name: "session",
                        value: process.env.session,
                    });
                    await page
                        .goto(url, {
                            timeout: 10000,
                        })
                        .catch((error: Error): void => {
                            console.error(error);
                        });
                    await page.waitForTimeout(1000);
                    setTimeout(() => {
                        bot.close();
                    }, 30000);
                })("http://web:8000" + data);
                console.log("> Job Done.");
            }
        } catch (error) {
            console.log("> " + error);
        }
    }
})();
