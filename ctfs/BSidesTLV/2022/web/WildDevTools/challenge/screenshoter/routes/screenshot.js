import puppeteer from 'puppeteer';
import log from '../utils/logger.js';
import getRandomPort from '../utils/get-random-port.js';

async function getBrowserWithTimeout(seconds) {
    log('launching browser...');
    let browser = null;

    for (let i = 0; i < 5; i++) {
        if (browser !== null) {
            continue;
        }
        try {
            browser = await puppeteer.launch({
                timeout: 5000,
                headless: true,
                ignoreDefaultArgs: [
                    '--disable-popup-blocking'
                ],
                args: [
                    '--no-sandbox',
                    '--ignore-certificate-errors',
                    '--disable-setuid-sandbox',
                    '--disable-accelerated-2d-canvas',
                    '--disable-gpu',
                    '--proxy-server=smokescreen:4750',
                    `--remote-debugging-port=${getRandomPort()}`
                ]
            });
        } catch (err) {
            browser = null;
            log(err);
        }
    }

    setTimeout(async () => {
        try {
            await browser.close();
        } catch (err) {
            log('browser.close() failed:', err.message);
        }
    }, seconds * 1000);

    log(`browser is ready, closing it in ${seconds} seconds.`);

    return browser;
}

export default async function handleScreenshotRequest(req, res) {
    try {
        log('req.query.url', req.query.url);

        const timeout = parseInt(process.env.BROWSER_TIMEOUT) || 30;
        const browser = await getBrowserWithTimeout(timeout);

        const page = await browser.newPage();
        await page.goto(req.query.url, { waitUntil: 'networkidle0' });

        log('taking a screenshot...');

        const image = await page.screenshot({
            quality: 100,
            type: 'jpeg',
            fullPage: true
        });

        log('generating response...');

        res.writeHead(200, {
            'Content-Type': 'image/jpeg',
            'Content-Length': image.length
        });

        res.end(image);

        log('done!');
    } catch (err) {
        log('unexpected error', err);
        res.status(500).json({ error: 'unexpected error' });
    }
}