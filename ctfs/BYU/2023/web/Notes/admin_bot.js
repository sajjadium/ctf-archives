const express = require('express');
const puppeteer = require('puppeteer');
const escape = require('escape-html');
const fs = require('fs');

const app = express()
app.use(express.urlencoded({ extended: true }));

const SECRET = fs.readFileSync('secret.txt', 'utf8').trim()

const visitUrl = async (url) => {

    let browser =
            await puppeteer.launch({
                headless: "new",
                pipe: true,
                dumpio: true,

                // headless chrome in docker is not a picnic
                args: [
                    '--no-sandbox',
                    '--disable-gpu',
                    '--disable-software-rasterizer',
                    '--disable-dev-shm-usage',
                    '--disable-setuid-sandbox',
                    '--js-flags=--noexpose_wasm,--jitless'
                ]
            })

    try {
        const page = await browser.newPage()

        try {
            await page.setUserAgent('puppeteer');
            
            // login
            await page.goto('http://127.0.0.1:1337/login', { timeout: 5000, waitUntil: 'networkidle2' })
            await page.type('#username', 'admin');
            await page.type('#password', SECRET);
            await Promise.all([
                page.click('#formsubmit'),
                page.waitForNavigation({ waitUntil: 'networkidle0' }),
            ]);

            // visit the page
            await page.goto(url, { timeout: 5000, waitUntil: 'networkidle2' })
        } finally {
            await page.close()
        }
    }
    finally {
        browser.close()
        return
    }
}

app.get('/', async (req, res) => {
    html = `
    <html>
    <head>
        <title>Admin bot</title>
    </head>
    <style>
    body {
        background-color: black;
        color: white;
        font-family: Arial, sans-serif;
    }
    
    .container {
        max-width: 800px;
        margin: 0 auto;
        text-align: center;
        padding: 20px;
    }
    
    h1 {
        font-size: 36px;
        margin-bottom: 20px;
    }
    
    form {
        display: inline-block;
        text-align: left;
    }
    
    label {
        display: block;
        margin-bottom: 10px;
    }
    
    #path_box {
        display: flex;
        align-items: center;
        width: 100%;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 5px;
        border: none;
        background-color: #f2f2f2;
        color: black;
        font-size: 18px;
    }

    input {
        flex-grow: 1;
        font-size: 18px;
        border: none;
    }
    
    button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        font-size: 18px;
        cursor: pointer;
    }
    
    button:hover {
        background-color: #3e8e41;
    }
    </style>
    <body>
        <br><br><br>
        <div class="container">
            <h1>Have the admin bot visit a page</h1>
            <div id="path_box">
                <input type="text" id="path" name="path" size="50">
            </div>
            <button onclick="go()">Go</button>
        </div>
        <script>
            async function go() {
                document.getElementsByTagName('button')[0].disabled = true;
                document.getElementsByTagName('button')[0].textContent = "Visiting page..."
                let path = document.getElementById('path').value
                await fetch('/visit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: 'path=' + encodeURIComponent(path)
                })
                .then(response => response.text())
                .then(text => {
                    alert(text)
                })
                document.getElementsByTagName('button')[0].textContent = "Go"
                document.getElementsByTagName('button')[0].disabled = false;
            }
        </script>
    </body>
    </html>
    <html>`
    res.send(html)
});

app.post('/visit', async (req, res) => {
    const path = req.body.path
    console.log('received path: ', path)

    try {
        console.log('visiting url: ', path)
        await visitUrl(path)
    } catch (e) {
        console.log('error visiting: ', path, ', ', e.message)
        res.send('Error visiting page: ' + escape(e.message))
    } finally {
        console.log('done visiting url: ', path)
        res.send('Visited page.')
    }
});

const port = 1336
app.listen(port, async () => {
    console.log(`Listening on ${port}`)
})