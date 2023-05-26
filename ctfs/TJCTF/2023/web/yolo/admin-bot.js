import flag from './flag.txt';

function sleep(time) {
    return new Promise(resolve => {
        setTimeout(resolve, time);
    });
}

export default {
    id: 'yolo',
    name: 'yolo',
    urlRegex: /^https:\/\/yolo\.tjc\.tf\//,
    timeout: 10000,
    handler: async (url, ctx) => {
        const page = await ctx.newPage();
        await page.goto('https://yolo.tjc.tf', { waitUntil: 'domcontentloaded' });

        await sleep(1000);

        await page.type('#name', 'admin');
        await page.type('#toDo', flag.trim());

        await page.click('#submit');

        await sleep(500);

        await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' });
        await sleep(3000);
    }
};
