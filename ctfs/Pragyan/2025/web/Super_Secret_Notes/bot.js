import { promises as fs } from 'fs';
import puppeteer from 'puppeteer';
import express from 'express';
import 'dotenv/config';

const app = express();
app.use(express.json());

(async () => {
    let flag;
    try {
        flag = await fs.readFile('./flag.txt', 'utf-8');
    } catch (error) {
        process.exit(1); 
    }

    async function visitUrl(url) {
        const browser = await puppeteer.launch({
            headless: 'new',
            args: ['--no-sandbox'],
        });

        try {
            const page = await browser.newPage();

            await page.goto(process.env.SERVER_URL, {
                waitUntil: 'domcontentloaded',
                timeout: 3000,
            });

            await page.evaluate((flag) => {
                localStorage.setItem('flag', flag);
            }, flag);

            await page.goto(url, {
                waitUntil: 'domcontentloaded',
                timeout: 3000,
            });

            await new Promise((resolve) => setTimeout(resolve, 3000));
        } catch (error) {

        } finally {
            await browser.close();
        }
    }

    app.post('/submit', async (req, res) => {

        const { url } = req.body;

        if (!url.match(process.env.SERVER_REGEX_HTTP) && !url.match(process.env.SERVER_REGEX_HTTPS)) {            return res.status(400).json({ error: 'Invalid URL format' });
        }
        try {
            await visitUrl(url);
            res.json({ success: true, message: 'Admin bot visited your URL' });
        } catch (error) {
            res.status(500).json({ error: 'Failed to process URL' });
        }
    });

    const PORT = 3000;
    app.listen(PORT, () => {
        console.log(`Admin bot server is running on http://localhost:${PORT}`);
    });
})();
