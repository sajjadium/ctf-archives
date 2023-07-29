import puppeteer from 'puppeteer-extra'
import puppeteer_user_preferences from 'puppeteer-extra-plugin-user-preferences'

const sleep = time => new Promise(resolve => setTimeout(resolve, time));

puppeteer.use(puppeteer_user_preferences({
    userPrefs: {
        net: {
            network_prediction_options: 2
        }
    }
}));

async function visit(url) {
    const browser = await puppeteer.launch({
        executablePath: '/usr/bin/chromium-browser',
        headless: 'new',
        pipe: true,
        dumpio: true,
        args: [
            '--js-flags=--jitless',
            '--disable-gpu',
            '--enable-experimental-web-platform-features',
            '--incognito'
        ]
    });

    const page = await browser.newPage();

    await Promise.race([(async() => {
        try {
            await page.goto(url);
            await page.evaluate(async flag => {
                window.win(flag);
            }, process.env.FLAG ?? 'corctf{test_flag}');
            await sleep(5000);
        } catch(e) {};
    })(), sleep(10000)]);

    await browser.close();
}

visit(process.env.URL);