const puppeteer = require('puppeteer');

(async () => {
  try {
    const browser = await puppeteer.launch({
      headless: "new",
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 1200, height: 1600 });

    // 1. 10links (Clean Homepage)
    console.log('Visiting 10links.blue...');
    await page.goto('https://10links.blue', { waitUntil: 'networkidle2' });
    await page.screenshot({ path: '10links_clean.png' });

    // 2. Bing (Cluttered Search) - Easier than Google to scrape
    console.log('Visiting Bing...');
    await page.goto('https://www.bing.com/search?q=best+credit+cards', { waitUntil: 'networkidle2' });
    await page.screenshot({ path: 'bing_clutter.png' });

    await browser.close();
  } catch (error) {
    console.error(error);
    process.exit(1);
  }
})();
