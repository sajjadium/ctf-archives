async (url, ctx) => {
    let page = await ctx.newPage();

    await page.goto("http://localhost:1337", {
        waitUntil: "domcontentloaded"
    });

    await page.evaluate(flag => {
        window.localStorage.setItem("initialised", true);
        window.localStorage.setItem("blockHistory", JSON.stringify({
            "1592953200000": {
                "url": flag,
                "numBlocked": 9876734123
            }
        }));
    }, "idek{REDACTED}");

    await page.goto(url, {
        waitUntil: "domcontentloaded"
    });

    await page.waitForTimeout(10000);
}