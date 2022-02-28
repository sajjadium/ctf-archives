const opt = {
    name: "fxxkcors",
    router: "fxxkcors",
    site: process.env.FXXK_SITE ?? "",

}

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

const visit = async (browser, url) =>{
    let site = process.env.FXXK_SITE ?? ""
    console.log(`[+]${opt.name}: ${url}`)
    let renderOpt = {...opt}
    try {
        const loginpage = await browser.newPage()
        await loginpage.goto(site)
        await loginpage.type("input[name=username]", "admin")
        await loginpage.type("input[name=password]", process.env.FXXK_ADMIN_PASS ?? "")
        await Promise.all([
            loginpage.click('button[name=submit]'),
            loginpage.waitForNavigation({waitUntil: 'networkidle0', timeout: 2000})
        ])
        await loginpage.goto("about:blank")
        await loginpage.close()

        const page = await browser.newPage()
        await page.goto(url, {waitUntil: 'networkidle0', timeout: 2000})

        await delay(2000) /// waiting 2 second.
        console.log(await page.evaluate(() =>  document.documentElement.outerHTML))

    }catch (e) {
        console.log(e)
        renderOpt.message = "error occurred"
        return renderOpt
    }
    renderOpt.message = "admin will view your report soon"
    return renderOpt
}

module.exports = {
    opt:opt,
    visit:visit
}