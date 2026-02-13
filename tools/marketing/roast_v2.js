const puppeteer = require('puppeteer');

(async () => {
  try {
    const browser = await puppeteer.launch({
      headless: "new",
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    
    // Set realistic User-Agent to bypass simple bot checks
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
    await page.setViewport({ width: 1280, height: 1600 });

    // --- 1. 10links.blue (Fixing the 404) ---
    console.log('Visiting 10links.blue homepage...');
    await page.goto('https://10links.blue', { waitUntil: 'networkidle2' });
    
    // Find search box (usually input type text or search)
    // We'll try to find input, type, and submit
    const searchSelector = 'input[type="text"], input[type="search"]';
    await page.waitForSelector(searchSelector);
    await page.type(searchSelector, 'best credit cards');
    await page.keyboard.press('Enter');
    
    console.log('Waiting for 10links results...');
    await page.waitForNavigation({ waitUntil: 'networkidle2' });
    
    await page.screenshot({ path: '10links_v2.png' });
    console.log('Saved 10links_v2.png');

    // --- 2. Google (Attempting bypass) ---
    console.log('Visiting Google...');
    await page.goto('https://www.google.com/search?q=best+credit+cards&hl=en', { waitUntil: 'networkidle2' });
    
    // Check for "Accept all" (Consent)
    try {
      const consentBtn = await page.$x("//button[contains(., 'Accept all')]");
      if (consentBtn.length > 0) {
        await consentBtn[0].click();
        await page.waitForNavigation();
      }
    } catch (e) {}

    await page.screenshot({ path: 'google_v2.png' });
    console.log('Saved google_v2.png');

    await browser.close();
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
})();
