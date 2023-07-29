import flag from './flag.txt'

function sleep(time) {
  return new Promise(resolve => {
    setTimeout(resolve, time)
  })
}

export default {
  name: 'youdirect admin bot',
  urlRegex: /^https:\/\/youtube\.com\//,
  timeout: 10000,
  handler: async (url, ctx) => {
    const page = await ctx.newPage();
    await page.goto(url, { waitUntil: 'domcontentloaded' });
    await sleep(2000);
    await page.evaluate(flag => {
      window.win(flag);
    }, flag);
    await sleep(1000);
  }
}