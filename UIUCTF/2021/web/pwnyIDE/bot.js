/*
NOTE: this is the script that the admin bot runs to visit your provided URL
*/

import { chromium } from "playwright-chromium"

(async function () {
  console.log("launching browser...")
  const browser = await chromium.launch({
    logger: {
      isEnabled: () => true,
      log: (name, severity, message, _args) => console.log(`chrome log: [${name}/${severity}] ${message}`)
    }
  })
  let url = process.argv[2].trim()
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    process.exit(1)
  }
  const context = await browser.newContext() // "incognito" by default
  const page = await context.newPage()
  await page.goto(url)
  setTimeout(() => {
    try {
      page.close()
      browser.close()
      console.log("successful run")
      process.exit()
    } catch (err) {
      console.log(`err: ${err}`)
      process.exit(1)
    }
  }, 5000);
})();
