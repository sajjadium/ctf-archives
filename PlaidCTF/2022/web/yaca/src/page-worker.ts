import * as puppeteer from "puppeteer";
import * as fs from "fs/promises";
import * as path from "path";

import { dequeue } from "./database";

const flag = process.env.FLAG ?? "flag{missing}"

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

const visitOne = async () => {
    const url = await dequeue();
    if (url === undefined) {
        await sleep(500);
        return;
    }

    const browser = await puppeteer.launch({
        dumpio: true,
        pipe: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    await page.setCookie({
        name: "flag",
        value: flag,
        domain: "localhost:3838",
    })

    await Promise.race([
        page.goto(url),
        sleep(3000),
    ]);
    await sleep(3000);

    await browser.close();
}

export const startVisiting = async () => {
    while (true) {
        try {
            await visitOne();
        } catch (e) {
            console.error(e);
        }
    }
}

