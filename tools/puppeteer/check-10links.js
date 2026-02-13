const puppeteer = require('puppeteer');

(async () => {
  try {
    const browser = await puppeteer.launch({
      headless: "new",
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    console.log('Navigating to https://10links.blue...');
    await page.goto('https://10links.blue', { waitUntil: 'networkidle2' });
    
    const title = await page.title();
    console.log('Title:', title);
    
    // Screenshot
    await page.screenshot({ path: '10links.png', fullPage: true });
    console.log('Screenshot saved to 10links.png');
    
    await browser.close();
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
})();
