const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  try {
    const browser = await puppeteer.launch({
      headless: "new",
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    
    // 1. Take Product Hunt Hero Screenshot
    const phHeroPath = path.resolve(__dirname, '../../assets/product-hunt-hero.html');
    const phHeroUrl = 'file://' + phHeroPath;
    console.log(`Navigating to ${phHeroUrl}`);
    await page.setViewport({ width: 1200, height: 630 });
    await page.goto(phHeroUrl, { waitUntil: 'networkidle0' });
    
    // Wait a bit for any fonts or styles
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const phOutput = path.resolve(__dirname, '../../assets/product-hunt-hero.png');
    console.log(`Saving to ${phOutput}`);
    await page.screenshot({ path: phOutput });

    // 2. Take Landing Page Screenshot (Top Fold)
    const landingPath = path.resolve(__dirname, '../../index.html');
    const landingUrl = 'file://' + landingPath;
    console.log(`Navigating to ${landingUrl}`);
    await page.setViewport({ width: 1440, height: 900 });
    await page.goto(landingUrl, { waitUntil: 'networkidle0' });

    // Wait for any JS (like stars) to load? Or just wait 1s.
    await new Promise(resolve => setTimeout(resolve, 1000));

    const landingOutput = path.resolve(__dirname, '../../assets/landing-page-hero.png');
    console.log(`Saving to ${landingOutput}`);
    await page.screenshot({ path: landingOutput });

    // 3. Take Full Page Screenshot (for reference/audit)
    const landingFullOutput = path.resolve(__dirname, '../../assets/landing-page-full.png');
    console.log(`Saving full page to ${landingFullOutput}`);
    await page.screenshot({ path: landingFullOutput, fullPage: true });

    await browser.close();
    console.log('Done.');
  } catch (err) {
    console.error('Error:', err);
    process.exit(1);
  }
})();
