#!/usr/bin/env python3
"""Automate RentAHuman bounty payment"""
import asyncio
from playwright.async_api import async_playwright

CHROME_PATH = "/home/barrowryan89/chrome-extracted/opt/google/chrome/chrome"

async def pay_bounty():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Navigate to bounty
        await page.goto("https://rentahuman.ai/bounties/J5yx5AUxT7TIK8PY9JzO")
        print("Loaded bounty page")
        
        # Wait for login or payment button
        await asyncio.sleep(5)
        
        # Screenshot for verification
        await page.screenshot(path="/tmp/bounty_screenshot.png")
        print("Screenshot saved")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(pay_bounty())
