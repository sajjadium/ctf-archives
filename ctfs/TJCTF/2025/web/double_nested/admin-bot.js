import flag from './flag.txt';

function sleep(time) {
    return new Promise(resolve => {
        setTimeout(resolve, time)
    });
}

export default {
    id: 'double-nested',
    name: 'double-nested',
    urlRegex: /^https:\/\/double-nested\.tjc\.tf\//,
    timeout: 10000,
    handler: async (url, ctx) => {
        const page = await ctx.newPage();
        await page.goto(url + flag, { timeout: 3000, waitUntil: 'domcontentloaded' });
        await sleep(5000);
    }
};
