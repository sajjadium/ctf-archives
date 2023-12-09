import os
import asyncio
from playwright.async_api import async_playwright
from flask import Flask, render_template, request

app = Flask(__name__)

DOMAIN = "nginx"
FLAG = os.environ.get("FLAG", "TsukuCTF23{**********REDACTED**********}")


@app.route("/crawler", methods=["GET"])
def index_get():
    return render_template("index_get.html")


async def crawl(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            response = await page.goto(url, timeout=5000)
            header = await response.header_value("Server")
            content = await page.content()

            if ("Tsukushi/2.94" in header) and ("🤪" not in content):
                await page.context.add_cookies(
                    [{"name": "FLAG", "value": FLAG, "domain": DOMAIN, "path": "/"}]
                )
                if url.startswith(f"http://{DOMAIN}/?code=") or url.startswith(
                    f"https://{DOMAIN}/?code="
                ):
                    await page.goto(url, timeout=5000)
        except:
            pass

        await browser.close()


@app.route("/crawler", methods=["POST"])
def index_post():
    asyncio.run(
        crawl(
            request.form.get("url").replace(
                "http://localhost:31416/", f"http://{DOMAIN}/", 1
            )
        )
    )
    return render_template("index_post.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=31417)
