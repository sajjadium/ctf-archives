const crypto = require("crypto");

module.exports = {
    name: "antisocial-media",
    async execute(browser, url) {
        const page = await browser.newPage();

        // Sets the FLAG cookie.
        await page.setCookie({
            name: "secret",
            value: process.env.CHALL_ANTISOCIAL_MEDIA_ADMIN_PW || "placeholder",
            domain: process.env.CHALL_ANTISOCIAL_MEDIA_DOMAIN || "localhost",
            httpOnly: true,
            sameSite: "Lax",
        });

        // Logins to the site.
        await page.goto(process.env.CHALL_ANTISOCIAL_MEDIA_URL || "http://localhost:3000");
        await page.waitForSelector("#username");
        await page.type("#username", crypto.randomBytes(32).toString("hex"));
        await page.type("#password", crypto.randomBytes(32).toString("hex"));
        await page.click("#login");
        await page.waitForNavigation();

        // Visits the given URL.
        await page.goto(url);
        await page.waitForNetworkIdle({
            timeout: 10000,
        });
        await page.close();
    },
};
