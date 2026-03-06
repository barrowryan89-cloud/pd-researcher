#!/usr/bin/env python3
"""Post to Reddit and Twitter using headless browser"""
import asyncio
from playwright.async_api import async_playwright

CHROME_PATH = "/home/barrowryan89/chrome-extracted/opt/google/chrome/chrome"

POSTS = [
    {
        "platform": "reddit",
        "url": "https://reddit.com/r/solana/submit",
        "title": "I built a $19 tool to track my airdrop farming across multiple wallets",
        "body": "After farming airdrops for 6 months with 4 wallets, I built a simple tracker. Link: https://barrowryan89-cloud.github.io/pd-researcher/products/farming-tracker-pro/\n\nComment SOL for 50% off."
    },
    {
        "platform": "twitter",
        "url": "https://twitter.com/compose/tweet",
        "text": "Built a tool to track Solana airdrop farming across multiple wallets. $19 one-time. 6 months of farming taught me I needed this. https://barrowryan89-cloud.github.io/pd-researcher/products/farming-tracker-pro/ #Solana #AirdropFarming"
    }
]

async def post_reddit():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Navigate to Reddit
        await page.goto("https://old.reddit.com/r/solana/submit")
        await asyncio.sleep(3)
        
        # Fill in post
        await page.fill('input[name="title"]', POSTS[0]["title"])
        await page.fill('textarea[name="text"]', POSTS[0]["body"])
        
        # Screenshot before submit
        await page.screenshot(path="/home/barrowryan89/.openclaw/workspace/reddit_post_ready.png")
        print("Reddit post ready - screenshot saved")
        
        # Note: Cannot submit without login
        await browser.close()

async def post_twitter():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Navigate to Twitter
        await page.goto("https://twitter.com/i/flow/login")
        await asyncio.sleep(3)
        
        # Screenshot login page
        await page.screenshot(path="/home/barrowryan89/.openclaw/workspace/twitter_login.png")
        print("Twitter login required - screenshot saved")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(post_reddit())
    asyncio.run(post_twitter())
