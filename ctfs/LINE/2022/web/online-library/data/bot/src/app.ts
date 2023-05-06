import * as Puppeteer from "puppeteer";
import * as Redis from "ioredis";
import * as Url from "url";

const redis: Redis.Redis = new Redis(6379, "redis");

(async (): Promise<void> => {
    while (true) {
        const [error, data]: Array<string> = await redis.blpop("query", 0)
        if (data && data.startsWith("/") && Url.parse("http://web" + data).host === "web") {
            console.log("> Start to process - http://web" + data)
            await(
                async (url: string): Promise<void> => {
                const bot: Puppeteer.Browser = await Puppeteer.launch({
                    product: "chrome",
                    headless: true,
                    ignoreHTTPSErrors: true,
                    args: ["--no-sandbox"]
                })
                const page: Puppeteer.Page = await bot.newPage();
                await page.setCookie({
                    domain: "web",
                    name: "FLAG",
                    value: process.env.FLAG
                })
                await page.goto(url, {
                    timeout: 10000
                }).catch((error: Error): void => {
                    console.error(error)
                })
                await page.close()
                await bot.close()
            })("http://web" + data);
            console.log("> Job Done.")
        } else {
            console.error("> Invalid path.")
        }
    }
})();