from pyppeteer import launch
import asyncio


async def visit(order_id):
    url = f'http://web:8080/orders/{order_id}/preview'
    print("Visiting", url)
    browser = await launch({'args': ['--no-sandbox', '--disable-setuid-sandbox']})
    page = await browser.newPage()
    await page.goto(url)
    await asyncio.sleep(3)
    await browser.close()