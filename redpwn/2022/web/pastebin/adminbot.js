import flag from './flag.txt'

export default {
  id: 'pastebin',
  name: 'pastebin',
  timeout: 10000,
  handler: async (url, ctx) => {
    const page = await ctx.newPage()
    await page.setCookie({ name: 'flag', value: flag.trim(), domain: 'pastebin.mc.ax' })
    await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(5000)
  },
}
