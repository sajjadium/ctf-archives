import flag from './server/flag.txt';

const sleep = (time) => new Promise((resolve) => setTimeout(resolve, time));

export default {
  id: 'dnu-merch',
  name: 'dnu-merch',
  timeout: 154000,
  handler: async (url, ctx) => {
    const page = await ctx.newPage();
    await page.setCookie({
      domain: 'dnu-merch.tjc.tf',
      name: 'items',
      value: JSON.stringify([{ title: flag.trim(), cost: 100000 }]),
      secure: true,
      sameSite: 'None',
    });
    await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' });
    await sleep(150000);
  },
};
