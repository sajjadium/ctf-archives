from pyppeteer import launch
import asyncio


async def visit(user_id, admin_token):
    url = f'http://web:8080/profile/{user_id}'
    print("Visiting", url)
    browser = await launch({'args': ['--no-sandbox', '--disable-setuid-sandbox']})
    page = await browser.newPage()
    await page.setCookie({'name': 'admin_token', 'value': admin_token, 'url': 'http://web:8080', 'httpOnly': True, 'sameSite': 'Strict'})
    await page.goto(url)
    await asyncio.sleep(3)
    await browser.close()
