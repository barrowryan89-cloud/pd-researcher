#!/usr/bin/env python3
"""
Social Media Automation with Playwright
Posts to Twitter/X, Reddit, LinkedIn using headless browser
"""
import asyncio
from playwright.async_api import async_playwright

CHROME_PATH = "/home/barrowryan89/chrome-extracted/opt/google/chrome/chrome"

class SocialPoster:
    def __init__(self):
        self.browser = None
        self.context = None
    
    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True
        )
        self.context = await self.browser.new_context()
    
    async def post_twitter(self, username, password, text):
        """Post to Twitter/X"""
        page = await self.context.new_page()
        
        # Login
        await page.goto("https://twitter.com/login")
        await page.fill('input[name="text"]', username)
        await page.click('//span[text()="Next"]')
        await page.fill('input[name="password"]', password)
        await page.click('//span[text()="Log in"]')
        
        # Post
        await page.fill('div[data-testid="tweetTextarea_0"]', text)
        await page.click('button[data-testid="tweetButton"]')
        
        await page.close()
        return True
    
    async def post_reddit(self, subreddit, title, text):
        """Post to Reddit"""
        page = await self.context.new_page()
        
        # Navigate to submit page
        await page.goto(f"https://reddit.com/r/{subreddit}/submit")
        
        # Fill post
        await page.fill('textarea[placeholder="Title"]', title)
        await page.fill('div[role="textbox"]', text)
        await page.click('button[type="submit"]')
        
        await page.close()
        return True
    
    async def close(self):
        await self.browser.close()
        await self.playwright.stop()

if __name__ == "__main__":
    import sys
    
    async def main():
        poster = SocialPoster()
        await poster.start()
        
        if len(sys.argv) < 2:
            print("Usage: social_poster.py <platform> <args>")
            print("  twitter <username> <password> <text>")
            print("  reddit <subreddit> <title> <text>")
            await poster.close()
            return
        
        platform = sys.argv[1]
        
        if platform == "twitter":
            await poster.post_twitter(sys.argv[2], sys.argv[3], sys.argv[4])
            print("✅ Twitter post scheduled")
        elif platform == "reddit":
            await poster.post_reddit(sys.argv[2], sys.argv[3], sys.argv[4])
            print("✅ Reddit post scheduled")
        
        await poster.close()
    
    asyncio.run(main())
