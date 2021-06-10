import * as assert from 'assert';
import * as massive from 'massive';
import {Builder, By} from 'selenium-webdriver';
import * as firefox from 'selenium-webdriver/firefox';
import {UserPromptHandler} from 'selenium-webdriver/lib/capabilities';
import {URL} from 'url';

assert.ok(process.env.SITE_URL, 'SITE_URL is not set');
assert.ok(process.env.ADMIN_PASSWORD, 'ADMIN_PASSWORD is not set');
assert.ok(process.env.DB, 'DB is not set');

function timeout(delay: number) {
  return new Promise(resolve => setTimeout(resolve, delay));
}

async function checkReport(id: string, baseUrl: string, adminPassword: string) {
  console.log(`Checking ${new URL(`/notes/${id}`, baseUrl)}`);
  const driver = new Builder()
                     .forBrowser('firefox')
                     .setFirefoxOptions(
                         new firefox.Options().headless().setAlertBehavior(
                             UserPromptHandler.DISMISS) as firefox.Options)
                     .build();
  try {
    console.log('Logging in');
    await driver.get(new URL('/login', baseUrl).toString());
    let el = await driver.findElement(By.id('name'));
    await el.sendKeys('admin');
    el = await driver.findElement(By.id('password'));
    await el.sendKeys(adminPassword);
    el = await driver.findElement(By.id('submit'));
    await el.click();

    console.log('Visiting report');
    await driver.get(new URL(`/notes/${id}`, baseUrl).toString());
    await driver.sleep(30 * 1000);
  } finally {
    await driver.quit();
  }
}

async function main() {
  const db = await massive(process.env.DB);

  while (true) {
    const reports = await db.reports.destroy();
    console.log(`Got ${reports.length} reports`);
    for (let report of reports) {
      await checkReport(
          report.id, process.env.SITE_URL, process.env.ADMIN_PASSWORD)
          .catch(console.log);
    }
    await timeout(5000);
  }
}

main();
