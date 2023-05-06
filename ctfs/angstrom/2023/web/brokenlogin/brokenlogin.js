module.exports = {
    name: "brokenlogin",
    timeout: 7000,
    async execute(browser, url) {
        if (!/^https:\/\/brokenlogin\.web\.actf\.co\/.*/.test(url)) return;
        
        const page = await browser.newPage();

        await page.goto(url);
        await page.waitForNetworkIdle({
            timeout: 5000,
        });

        await page.waitForSelector("input[name=username]");
        
        await page.$eval(
          "input[name=username]",
          (el) => (el.value = "admin")
        );

        await page.waitForSelector("input[name=password]");

        await page.$eval(
          "input[name=password]",
          (el, password) => (el.value = password),
          process.env.CHALL_BROKENLOGIN_FLAG
        );

        await page.click("input[type=submit]");

        await new Promise((r) => setTimeout(r, 1000));

        await page.close();
    },
};
