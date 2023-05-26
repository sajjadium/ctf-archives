import flag from './flag.txt';

function sleep(time) {
    return new Promise(resolve => {
        setTimeout(resolve, time);
    });
}

export default {
    id: 'painter',
    name: 'painter',
    urlRegex: /^https:\/\/painter\.tjc\.tf\//,
    timeout: 10000,
    handler: async (url, ctx) => {
        const page = await ctx.newPage();
        await page.goto('https://painter.tjc.tf', { waitUntil: 'domcontentloaded' });

        await page.setCookie({
            name: 'flag',
            value: flag.trim(),
            domain: 'painter.tjc.tf',
        });

        await sleep(1000);

        await page.goto(url, { timeout: 10000, waitUntil: 'domcontentloaded' });
        await sleep(10000);
    }
};
