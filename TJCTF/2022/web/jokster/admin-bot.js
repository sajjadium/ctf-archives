import adminPassword from './server/admin-password.txt';

function sleep(time) {
    return new Promise(resolve => {
        setTimeout(resolve, time)
    });
}

export default {
    id: 'jokster',
    name: 'jokster',
    urlRegex: /^https:\/\/jokster\.tjc\.tf\//,
    timeout: 10000,
    handler: async (url, ctx) => {
        const page = await ctx.newPage();
        await page.goto('https://jokster.tjc.tf/login', { waitUntil: 'domcontentloaded' });

        await sleep(1000);

        const usernameInput = await page.$('#username');
        await usernameInput.type('admin');

        const passwordInput = await page.$('#password');
        await passwordInput.type(adminPassword.trim());

        const submitButton = await page.$('input[type="submit"]');
        await submitButton.click();

        await sleep(500);

        await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' });
        await sleep(3000);
    }
};
