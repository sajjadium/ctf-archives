// (snipped)

const flag = 'zer0pts{<censored>}';

// (snipped)

const crawl = async (url) => {
  console.log(`[+] Crawling started: ${url}`);

  try {
    const page = await browser.newPage();
    await page.setCookie({
      name: 'flag',
      value: flag,
      domain: 'challenge',
      httpOnly: false,
      secure: false
    });
    await page.goto(url, {
      waitUntil: 'networkidle0',
      timeout: 3 * 1000,
    });
    await page.close();
  } catch (e) {
    console.log('[-] ERROR');
    console.log('[-]', e);
  }

  console.log(`[+] Crawling finished: ${url}`);
};

// (snipped)
