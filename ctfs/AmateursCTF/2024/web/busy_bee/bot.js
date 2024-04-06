const sleep = time => new Promise(resolve => setTimeout(resolve, time))

const challenges = new Map([
  ['busy-bee', {
    name: 'Busy Bee',
    timeout: 10000,
    handler: async (url, ctx) => {
      const page = await ctx.newPage()
      await page.goto("https://busy-bee-amateurs-ctf-2024.pages.dev/", { timeout: 3000, waitUntil: 'domcontentloaded' })
      await page.evaluate(() => {
        localStorage.setItem("flag", "FLAG GOES HERE")
      })
      await page.goto("about:blank", {
        timeout: 3000,
        waitUntil: "domcontentloaded",
      });
      await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' })
      await sleep(2000)
      await page.evaluate(() => {
        document.querySelector("#controls :first-child").click();
      })

      await sleep(5000)
    },
    urlRegex: /^https:\/\/busy-bee-amateurs-ctf-2024\.pages\.dev/,
  }],
  
])

module.exports = {
  challenges
}
