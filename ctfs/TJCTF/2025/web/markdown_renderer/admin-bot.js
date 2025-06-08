import flag from './flag.txt';

function sleep(time) {
    return new Promise(resolve => {
        setTimeout(resolve, time)
    });
}

export default {
    id: 'markdown-renderer',
    name: 'markdown-renderer',
    urlRegex: /^https:\/\/markdown-renderer\.tjc\.tf\/markdown\/[a-z0-9-]+$/,
    timeout: 20000,
    handler: async (url, ctx) => {
        const page = await ctx.newPage();

        page.on('dialog', async dialog => {
            await dialog.accept();
        });

        // register the admin user
        await page.goto('https://markdown-renderer.tjc.tf/register', { timeout: 3000, waitUntil: 'domcontentloaded' });
        await page.type('#username', 'admin');
        await page.click('button[type="submit"]');

        await sleep(1000);

        // make new markdown file
        await page.type('#markdown', `# facts about me\ni love flags! (\`${flag.trim()}\`)\ni'm super locked in...`);
        await page.click('#renderButton')

        await sleep(1000);

        // go to your markdown file
        await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' });
        await sleep(1000);

        // open my own markdown file (better than yours)
        await page.click(`#markdownList>li>a`);

        await sleep(5000);
    }
};
