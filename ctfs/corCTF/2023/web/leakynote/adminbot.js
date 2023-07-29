import adminPassword from './admin_password.txt'

function sleep(time) {
  return new Promise(resolve => {
    setTimeout(resolve, time)
  })
}

export default {
  name: 'leakynote admin bot',
  timeout: 70000,
  handler: async (url, ctx) => {
    const page = await ctx.newPage();
    await page.goto("https://leakynote.be.ax/login.php", { waitUntil: 'domcontentloaded' });
    await sleep(2000);

    await page.type("input[name=name]", "admin");
    await page.type("input[name=pass]", adminPassword);
    await page.click("input[type=submit]");
    await sleep(2000);

    await page.goto(url, { waitUntil: 'domcontentloaded' });
    await sleep(65000);
  }
}