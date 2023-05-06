import flag from './flag.txt'

function sleep(time) {
  return new Promise(resolve => {
    setTimeout(resolve, time)
  })
}

export default {
  id: 'blazingfast',
  name: 'blazingfast',
  urlRegex: /^https:\/\/blazingfast\.mc\.ax\//,
  timeout: 10000,
  handler: async (url, ctx) => {
    const page = await ctx.newPage()
    await page.goto('https://blazingfast.mc.ax/', { timeout: 3000, waitUntil: 'domcontentloaded' })
    await page.evaluate(flag => localStorage.setItem('flag', flag), flag)
    await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' })
    await sleep(3000)
  }
}
