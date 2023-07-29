import flag from './chall/flag.txt'

function sleep(time) {
  return new Promise(resolve => {
    setTimeout(resolve, time)
  })
}

export default {
  name: 'crabspace admin bot',
  urlRegex: /^https:\/\/web-crabspace-crabspace-[0-9a-f]+\.be\.ax\/space\//,
  timeout: 10000,
  handler: async (url, ctx) => {
    const page = await ctx.newPage();
    
    const { origin } = new URL(url);
    await page.goto(`${origin}/login`, { waitUntil: 'domcontentloaded' });

    await page.type("input[name=name]", "admin");
    await page.type("input[name=pass]", flag);
    await page.click("input[type=submit]");

    await page.waitForSelector('textarea', { visible: true });

    await page.goto(url, { timeout: 5000, waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(5000);
  }
}