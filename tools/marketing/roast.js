const puppeteer = require('puppeteer');

(async () => {
  try {
    const browser = await puppeteer.launch({
      headless: "new",
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 1200, height: 1600 }); // Tall view

    // 1. Google (Ads & Clutter)
    console.log('Fetching Google results for "best credit cards"...');
    await page.goto('https://www.google.com/search?q=best+credit+cards', { waitUntil: 'networkidle2' });
    
    // Attempt to close cookie banner if present (simple selectors)
    try {
      await page.click('button[id="L2AGLb"]'); // Common "Accept all" button
    } catch (e) {
      // Ignore if not present
    }
    
    await page.screenshot({ path: 'google_clutter.png' });
    console.log('Saved google_clutter.png');

    // 2. 10links (Clean)
    console.log('Fetching 10links.blue results for "best credit cards"...');
    await page.goto('https://10links.blue/search?q=best+credit+cards', { waitUntil: 'networkidle2' });
    
    await page.screenshot({ path: '10links_clean.png' });
    console.log('Saved 10links_clean.png');

    await browser.close();
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
})();
