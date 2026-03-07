#!/usr/bin/env python3
"""Post to Reddit using headless browser"""
import asyncio
from playwright.async_api import async_playwright

CHROME_PATH = "/home/barrowryan89/chrome-extracted/opt/google/chrome/chrome"

async def post_reddit():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Navigate to Reddit
        await page.goto("https://reddit.com/r/solana/submit")
        
        print("Browser open. Please log in and post manually.")
        print("Title: I built a tool to track my airdrop farming across multiple wallets - $19")
        print("Body: https://barrowryan89-cloud.github.io/pd-researcher/products/farming-tracker-pro/")
        
        # Keep browser open for manual posting
        await asyncio.sleep(300)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(post_reddit())
