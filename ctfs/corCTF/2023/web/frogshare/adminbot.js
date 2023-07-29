import secrets from './secrets';

const username = "admin";
const { flag, password } = secrets;

export default {
    id: 'frogshare',
    name: 'frogshare',
    timeout: 20000,
    handler: async (url, ctx) => {
        const page = await ctx.newPage();
        await page.goto("https://frogshare.be.ax/login", { waitUntil: 'load' });

        await page.evaluate((flag) => {
            localStorage.setItem("flag", flag);
        }, flag);

        await page.type("input[name=username]", username);
        await page.type("input[name=password]", password);
        await Promise.all([
            page.waitForNavigation(),
            page.click("input[type=submit]")
        ]);
        /* No idea why the f this is required :| */
        await page.goto("https://frogshare.be.ax/frogs?wtf=nextjs", { timeout: 5000, waitUntil: 'networkidle0' });
        await page.waitForTimeout(2000);
        await page.goto(url, { timeout: 5000, waitUntil: 'networkidle0' });
        await page.waitForTimeout(5000);
    },
}
