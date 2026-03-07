#!/usr/bin/env python3
"""Find contact emails for crypto projects via multiple sources"""
import asyncio
from playwright.async_api import async_playwright

CHROME_PATH = "/home/barrowryan89/chrome-extracted/opt/google/chrome/chrome"

PROJECTS = ["marginfi", "kamino", "drift", "jupiter", "jito"]

async def find_contacts():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        for project in PROJECTS:
            # Try Twitter
            await page.goto(f"https://twitter.com/{project}")
            await asyncio.sleep(2)
            content = await page.content()
            
            # Look for email in bio or pinned tweet
            if "@" in content and ".com" in content:
                print(f"{project}: Possible email found in page content")
            else:
                print(f"{project}: No email visible")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(find_contacts())
