import flag from './flag.txt';
import crypto from 'crypto';

function sleep(time) {
    return new Promise(resolve => {
        setTimeout(resolve, time);
    });
}

export default {
    id: 'complainer',
    name: 'complainer',
    urlRegex: /^https:\/\/complainer\.tjc\.tf\//,
    timeout: 30000,
    handler: async (url, ctx) => {
        const page = await ctx.newPage();
        await page.goto('https://complainer.tjc.tf/register', { waitUntil: 'domcontentloaded' });

        await page.type('#username', crypto.randomBytes(16).toString('hex'));
        await page.type('#password', crypto.randomBytes(16).toString('hex'));

        await page.click('button[type="submit"]');

        await sleep(1000);

        await page.type('#body', flag.trim());
        await page.click('button[type="submit"]');

        await sleep(1000);

        await page.goto(url, { timeout: 10000, waitUntil: 'domcontentloaded' });
        await sleep(30000);
    }
};
