import flag from './flag.txt';

function sleep(time) {
    return new Promise(resolve => {
        setTimeout(resolve, time)
    });
}

export default {
    id: 'fleecebook',
    name: 'fleecebook',
    urlRegex: /^https:\/\/fleecebook\.tjc\.tf\//,
    timeout: 10000,
    handler: async (url, ctx) => {
        const page = await ctx.newPage();
        await page.setCookie({ domain: 'fleecebook.tjc.tf', name: 'flag', value: flag.trim() });
        await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' });
        await sleep(3000);
    }
};
