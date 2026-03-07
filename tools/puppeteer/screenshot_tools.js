const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  try {
    const browser = await puppeteer.launch({
      headless: "new",
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    
    // Navigate to the HTML file
    const fileUrl = 'file://' + path.resolve(__dirname, '../../assets/screenshot-studio/index.html');
    console.log(`Navigating to ${fileUrl}`);
    await page.goto(fileUrl, { waitUntil: 'networkidle0' });

    // Set viewport large enough
    await page.setViewport({ width: 1920, height: 3000 });

    // Selectors for the terminals
    const tools = [
      { id: '#port-scanner', name: 'port_scanner.png' },
      { id: '#json-formatter', name: 'json_formatter.png' },
      { id: '#html-cleaner', name: 'html_cleaner.png' }
    ];

    for (const tool of tools) {
      const element = await page.$(tool.id);
      if (element) {
        const outputPath = path.resolve(__dirname, '../../assets/tool_shots/', tool.name);
        console.log(`Saving screenshot for ${tool.id} to ${outputPath}`);
        await element.screenshot({ path: outputPath });
      } else {
        console.error(`Element ${tool.id} not found!`);
      }
    }

    await browser.close();
  } catch (err) {
    console.error('Error running puppeteer script:', err);
    process.exit(1);
  }
})();
