import flag from './flag.txt'
import adminPassword from './admin_password.txt'

function sleep(time) {
  return new Promise(resolve => {
    setTimeout(resolve, time)
  })
}

export default {
  id: 'carrot',
  name: 'carrot',
  urlRegex: /^https:\/\//,
  timeout: 70000,
  extraFields: [
    { name: 'instance', displayName: 'Instance ID', placeholder: 'carrot-{THIS}.mc.ax', regex: '^[0-9a-f]{1,32}$' }
  ],
  handler: async (url, ctx, { instance }) => {
    const page = await ctx.newPage()
    await page.goto(`https://carrot-${instance}.mc.ax`, { timeout: 3000, waitUntil: 'domcontentloaded' })
    
    await Promise.all([
      page.evaluate(({ username, password }) => {
        document.querySelector('[name="username"]').value = username;
        document.querySelector('[name="password"]').value = password;
        document.querySelector('[type="submit"]').click();
      }, {
        username: 'admin',
        password: adminPassword
      }),
      page.waitForNavigation({ waitUntil: 'domcontentloaded' })
    ])

    await page.goto('about:blank')

    await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' })

    await sleep(60000)
  }
}
