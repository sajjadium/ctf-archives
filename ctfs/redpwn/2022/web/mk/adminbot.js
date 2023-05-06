import flag from './flag.txt'

export default {
  id: 'mk',
  name: 'mk',
  timeout: 10000,
  handler: async (url, ctx) => {
    const page = await ctx.newPage()
		await page.setCookie({ name: 'flag', value: flag.trim(), domain: 'mk.mc.ax' })
		await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' })
		await page.waitForTimeout(5000)
  },
}
