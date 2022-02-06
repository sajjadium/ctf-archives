import FLAG from './flag.txt'
import FLAGPATH from './flagpath.txt'

// secret flag vault, same across runs of admin bot
const flagVault = FLAGPATH.split("/").map(x=>parseInt(x))

async function clickVault(page, i) {
    const vault = `a.vault-${i}`;
    const elem = await page.waitForSelector(vault, { visible: true })
    await Promise.all([page.waitForNavigation(), elem.click()])
}

async function navigateVault(page, path) {
    for (let i = 0; i < path.length; i++) {
        await clickVault(page, path[i])
    }
}

function sleep(time) {
    return new Promise(resolve => {
        setTimeout(resolve, time)
    })
}

export default {
    id: 'dicevault',
    name: 'dicevault',
    urlRegex: /.*/,
    timeout: 60000,
    handler: async (url, ctx) => {
        /*
           this handler is run with the provided url and a new puppeteer incognito latest-chromium browser context
           whenever someone submits a url to the admin bot
        */
        // go to the vault and put the flag there
        let page = await ctx.newPage()
        await page.goto('https://dicevault.mc.ax/', { timeout: 3000, waitUntil: 'domcontentloaded' })
        await navigateVault(page, flagVault)
        await page.type("#value", FLAG)
        await Promise.all([page.waitForNavigation(), page.click('#submit')])
        await page.close()

        // if we see a dicevault page, navigate to our vault :)
        ctx.on('targetcreated', async (target) => {
            if (target.type() === "page" && /^https:\/\/dicevault\.mc\.ax\/$/.test(target.url())) {
                await navigateVault(await target.page(), flagVault)
            }
        })

        // go to the provided url
        page = await ctx.newPage()
        await page.goto(url, { timeout: 5000, waitUntil: 'domcontentloaded' })
        await sleep(60000)
    }
}
