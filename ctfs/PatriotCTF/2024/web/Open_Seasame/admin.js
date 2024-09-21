const express = require("express");
const puppeteer = require("puppeteer");
const escape = require("escape-html");
const fs = require("fs");

const app = express();
app.use(express.urlencoded({ extended: true }));

const SECRET = fs.readFileSync("secret.txt", "utf8").trim();
const CHAL_URL = "http://127.0.0.1:1337/";

const visitUrl = async (url) => {
  let browser = await puppeteer.launch({
    headless: "new",
    pipe: true,
    dumpio: true,

    args: [
      "--no-sandbox",
      "--disable-gpu",
      "--disable-software-rasterizer",
      "--disable-dev-shm-usage",
      "--disable-setuid-sandbox",
      "--js-flags=--noexpose_wasm,--jitless",
    ],
  });

  try {
    const page = await browser.newPage();

    try {
      await page.setUserAgent("puppeteer");
      let cookies = [
        {
          name: "secret",
          value: SECRET,
          domain: "127.0.0.1",
          httpOnly: true,
        },
      ];
      await page.setCookie(...cookies);
      await page.goto(url, { timeout: 5000, waitUntil: "networkidle2" });
    } finally {
      await page.close();
    }
  } finally {
    browser.close();
    return;
  }
};

app.get("/", async (req, res) => {
  const html = `
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Bot</title>
        <style>
            body {
                background-color: #121212;
                color: #e0e0e0;
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                max-width: 600px;
                width: 100%;
                text-align: center;
                padding: 20px;
                background-color: #1e1e1e;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            }
            h1 {
                font-size: 32px;
                margin-bottom: 20px;
                color: #ff9800;
            }
            #path_box {
                display: flex;
                align-items: center;
                width: 100%;
                padding: 10px;
                margin-bottom: 20px;
                border-radius: 5px;
                background-color: #333;
            }
            #path_box div {
                color: #ff9800;
                margin-right: 10px;
            }
            input {
                flex-grow: 1;
                font-size: 16px;
                padding: 8px;
                border: none;
                border-radius: 4px;
                background-color: #555;
                color: #e0e0e0;
            }
            button {
                background-color: #ff9800;
                color: #1e1e1e;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 18px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            button:hover {
                background-color: #e68900;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Have the Admin Bot Visit a Page</h1>
            <div id="path_box">
                <div>http://127.0.0.1:1337/</div>
                <input type="text" id="path" name="path" placeholder="Enter the path">
            </div>
            <button onclick="go()">Go</button>
        </div>
        <script>
            async function go() {
                const button = document.querySelector('button');
                button.disabled = true;
                button.textContent = "Visiting page...";
                const path = document.getElementById('path').value;
                try {
                    const response = await fetch('/visit', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },
                        body: 'path=' + encodeURIComponent(path)
                    });
                    const text = await response.text();
                    alert(text);
                } catch (error) {
                    alert('An error occurred: ' + error.message);
                } finally {
                    button.textContent = "Go";
                    button.disabled = false;
                }
            }
        </script>
    </body>
    </html>`;
  res.send(html);
});

app.post("/visit", async (req, res) => {
  const path = req.body.path;
  console.log("received path: ", path);

  let url = CHAL_URL + path;

  if (url.includes("cal") || url.includes("%")) {
    res.send('Error: "cal" is not allowed in the URL');
    return;
  }

  try {
    console.log("visiting url: ", url);
    await visitUrl(url);
  } catch (e) {
    console.log("error visiting: ", url, ", ", e.message);
    res.send("Error visiting page: " + escape(e.message));
  } finally {
    console.log("done visiting url: ", url);
    res.send("Visited page.");
  }
});

const port = 1336;
app.listen(port, async () => {
  console.log(`Listening on ${port}`);
});
