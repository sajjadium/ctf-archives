const net = require('net');
const fs = require('fs');
const puppeteer = require('puppeteer');
const { hostname } = require('os');
const port = 1337;
const host = '0.0.0.0';
const FLAG = fs.readFileSync('./flag.txt', {encoding: 'utf-8'});
const WEBSITE = process.env['WEBSITE'] || 'website:5000'

const isValidUrl = (url) => (new URL(url).protocol == 'https:' || new URL(url).protocol == 'http:') && new URL(url).host == WEBSITE;

console.log(`Starting admin bot!`);

(async () => {
    const browser = await puppeteer.launch({
        executablePath: '/usr/bin/google-chrome-stable',
        headless: false,
        dumpio: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            //'--enable-logging=stderr',
            `--load-extension=./wiki-world`,
            //'--v=1',
            '--disable-extensions-except=./wiki-world',
        ]
    });
    const doAdminThing = async (url, sock) => {
        try {
            sock.write(`Admin is going to look at your note.\n`)
            const page = await browser.newPage();
            page
                .on('console', message =>
                console.log(`${message.type().substr(0, 3).toUpperCase()} ${message.text()}`))
                .on('pageerror', ({ message }) => console.log(message))
                .on('response', response =>
                console.log(`${response.status()} ${response.url()}`))
                .on('requestfailed', request =>
                console.log(`${request.failure().errorText} ${request.url()}`))
            await page.waitForTimeout(500);
            sock.write(`Clicking on ${url}.\n`)
            await page.goto(url, {
                waitUntil: 'networkidle2'
            });
            await page.waitForTimeout(500);
            await page.type('#note-input', '[INSERT WIKI-EXCERPT BLOB:Google] ' + FLAG);
            await page.waitForTimeout(9 * 1000);
            await page.click('#note-button');
            await page.waitForTimeout(9 * 1000);
            await page.close();
            sock.write('Admin closed page!\nNo issues where found!\n');
            sock.destroy();
        } catch(err) {
            console.log(err);
            sock.write(err.toString());
            sock.write('\nFailed to go to URL, please try again!\n');
            sock.destroy();
        }
    }
    const onClientConnection = async (sock) => {
        //Log when a client connnects.
        sock.write(`Please send the URL that you want to report: `);
        //Listen for data from the connected client.
        sock.on('data', async (data) => {
            data = data.toString().trim();
            try{
                if ( isValidUrl(data) ) {
                    await doAdminThing(data, sock);
                } else {
                    throw new Error('UrlNotvalid');
                }
            } catch(err) {
                console.log(err);
                sock.write(`Our admin thinks ${data} is not a valid URL to his site, so he has decided not to visit it!
Note: since our admin is in their weirdly configured server, all urls to the website start with http://website:5000\n`);
                sock.destroy();
            }
        });
        //Handle client connection termination.
        sock.on('close',() => {
            console.log(`Terminated the connection`);
        });
        //Handle Client connection error.
        sock.on('error',(error) => {
            console.error(`Connection Error ${error}`);
        });
    }

    const server = net.createServer(onClientConnection);
    console.log('Creating server!');

    server.listen(port, hostname, () => {
        console.log(`Server started on port ${port} at ${host}`); 
    });

    server.on('error', (err) => {
        console.log(err);
    });

})();
