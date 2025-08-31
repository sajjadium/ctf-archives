import password from './password.txt';

function sleep(time) {
  return new Promise(resolve => {
    setTimeout(resolve, time)
  })
}

export default {
  name: 'git admin bot',
  timeout: 15_000,
  urlRegex: /^https:\/\/git-[0-9a-f]+\.ctfi\.ng\//,
  handler: async (url, ctx) => {
    const base = new URL(url).origin

    let page = await ctx.newPage();
    await page.goto(base + '/login');
    await sleep(1000);
    await page.evaluate((password) => {
      document.getElementById('u').value = 'admin';
      document.getElementById('p').value = password;
      document.querySelector('form').submit();
    }, [password]);
    await sleep(5000);

    page = await ctx.newPage();
    await page.goto(url);
    await sleep(1000);
  }
}