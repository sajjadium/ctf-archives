var cron = require('node-cron');
var puppeteer = require("puppeteer")
const {sequelize,Message} = require("./models")
  
async function visitPage()
{
    var bot_user = process.env.BOT_USER;
    var bot_pass = process.env.BOT_PASSWORD;
    var frontend = process.env.FRONTEND_BOT
    const admin_video_id = "cb13a41b-04a1-47aa-8687-885fe74a1062"; //not the same on remote :)
    const admin_chat_id = "2e6e4787-6722-46da-83f9-8d38a4c7a922"; //not the same on remote :)
    const browser = await puppeteer.launch({
        headless: true,
        ignoreHTTPSErrors: true,
        args: ["--no-sandbox", "--ignore-certificate-errors" ],
        executablePath: "/usr/bin/chromium"
    });
    const page = await browser.newPage();
    await page.setDefaultNavigationTimeout(5000);
    await page.goto(`${frontend}/`)
    const username = await page.waitForSelector("#pseudo");
    const password = await page.waitForSelector("#password");

    await username.type(bot_user)
    await password.type(bot_pass)
    await page.keyboard.press("Enter");
    await page.waitForNavigation();
    await page.goto(`${frontend}/video/view/${admin_video_id}`)
    await Message.destroy({
        where: {
            chatId: admin_chat_id
        }
    })
    browser.close();
    return;
}

cron.schedule('*/1 * * * *', visitPage);