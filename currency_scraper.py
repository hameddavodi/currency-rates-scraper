import nest_asyncio
import asyncio
from playwright.async_api import async_playwright

nest_asyncio.apply()  # Allow nested event loops

async def open_url():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Set headless=True to run in background
        page = await browser.new_page()
        await page.goto("https://www.bonbast.com/")
        print("Page title:", await page.title())
        await browser.close()

# Run the script
if __name__ == '__main__':
    asyncio.run(main())
