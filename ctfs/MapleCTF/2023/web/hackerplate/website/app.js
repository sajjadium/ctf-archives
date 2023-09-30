import express from 'express';
import{ renderFile } from 'ejs';
import { marked } from 'marked';
import fs from 'fs';
import puppeteer from 'puppeteer';

const PORT = process.env.WEBSITE_PORT || 1337;

const app = express();

app.set('view engine', 'ejs');
app.engine('html', renderFile);
app.use(express.urlencoded({ extended: true }));

app.use(express.static('public'));

app.get("/", (req, res) => {
    // get all articles from the articles directory
    const articles = fs.readdirSync('articles').map(article => {
        const articleContent = fs.readFileSync(`articles/${article}`, 'utf8');
        const parts = articleContent.split('\n');
        const title = parts[0]
        const date = parts[1]
        const content = parts.slice(2).join('\n');
        const contentWithRedirects = content.replace(/(https?:\/\/[^\s]+)/g, `<a href="/redirect?url=$1">$1</a>`);
        const html = marked(contentWithRedirects);
        return { title, date, html}
    })
    res.render('index.ejs', { articles });
});

app.get("/redirect", (req, res) => {
    const url = req.query.url;
    // generate random nonce
    const nonce = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    const policies = [
        "default-src 'none'",
        `script-src 'nonce-${nonce}'`,
        "frame-src *",
        "style-src 'self'",
    ]
    res.set('Content-Security-Policy', policies.join(';'));
    res.render('redirect.ejs', { url, nonce });
});

app.get('/report', (req, res) => {
    res.render('report.ejs');
});

app.post('/report', (req, res) => {
    const { userUrl } = req.body;
    console.log(userUrl)
    try {
        const url = new URL(userUrl);
        if (!url.protocol.startsWith('http') && !url.protocol.startsWith('https')) {
            res.send('protocol doesnt look right');
            return;
        }
        if (url.hostname !== 'localhost' || url.port !== PORT) {
            res.send('not my business');
            return;
        }
        visit(url); // fast boi
        res.send("admin will take a look later today");
        return;l
    } catch (e) {
        console.log(e);
        res.send('Invalid URL');
        return;
    }
})

app.get('/healthz', (req, res) => {
    res.send("ok");
});

async function visit(url) {
    try {
        const browser = await puppeteer.launch({
            headless: 'new',
            args: [
                '--no-sandbox', 
                '--disable-setuid-sandbox',
            ],
            executablePath: process.env.CHROME_BIN || undefined,
        });
        const page = await browser.newPage();
        await page.goto(url.href);
        await page.waitForTimeout(5 * 1000);
        await page.close();
        await browser.close();
    } catch (e) {
        console.log(e);
    }
}


app.listen(PORT, () => {
    console.log(`website listening on port ${PORT}`);
});