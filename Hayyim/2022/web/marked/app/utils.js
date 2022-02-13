const webdriver = require('selenium-webdriver');
const capabilities = webdriver.Capabilities.chrome();

const flag = require('fs').readFileSync('/flag').toString().trim();

const rateLimit = 30 * 1000;
const pageTimeout = 3 * 1000;
const urlPrefix = 'http://marked:3000/';

const timestamps = new Map();

const sleep = (ms) => {
  return new Promise((resolve) => {
    setTimeout(() => resolve(), ms);
  });
};

const checkRateLimit = (key) => {
  const now = Date.now();

  if (timestamps.has(key) && timestamps.get(key) > now - rateLimit) {
    return false;
  }

  timestamps.set(key, now);
  return true;
};

const checkUrl = (url) => {
  return !(typeof url !== 'string' || !url.startsWith(urlPrefix));
};

const visitUrl = (url) => {
  return new Promise(async (resolve) => {
    const driver = new webdriver.Builder('chrome')
      .usingServer('http://selenium:4444/wd/hub/')
      .withCapabilities(capabilities)
      .build();

    await driver.get(urlPrefix);

    await driver.manage().addCookie({
      name: 'flag',
      value: flag
    });

    await driver.manage().setTimeouts({
      implicit: pageTimeout,
      pageLoad: pageTimeout,
      script: pageTimeout
    });

    await driver.get(url);
    await sleep(pageTimeout);
    await driver.quit();

    resolve();
  });
};

const checkParam = (param) => {
  if (typeof param !== 'string' || param.length === 0 || param.length > 256) {
    return false;
  }

  return true;
};

module.exports = {
  checkRateLimit,
  checkUrl,
  visitUrl,
  checkParam
};
