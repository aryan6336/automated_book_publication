# scrape_chapter.py

from playwright.sync_api import sync_playwright
import os

def scrape_chapter_from_url(url: str, save_path: str = "output/chapter1.txt") -> str:
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Screenshot for debugging (optional)
        page.screenshot(path="output/chapter1.png", full_page=True)

        # Extract visible text
        content = page.inner_text("body")

        # Save the chapter text
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(content)

        browser.close()
        print("✅ Chapter scraped and saved at:", save_path)

    return content

