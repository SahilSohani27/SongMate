from playwright.sync_api import sync_playwright
import time

def search_lyrics_and_scrape_with_ddg(song_name: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ))
        page = context.new_page()

        # ✅ Step 1: Search on Brave
        query = f"site:genius.com {song_name} lyrics"
        brave_url = f"https://duckduckgo.com/search?q={query.replace(' ', '+')}"
        print(f"[INFO] Searching on Brave: {brave_url}")
        page.goto(brave_url, timeout=15000)
        # time.sleep(15)
        # Wait for results and extract links
        page.wait_for_selector("a", timeout=10000)
        links = page.query_selector_all("a")

        genius_url = None
        for link in links:
            href = link.get_attribute("href")
            text = link.inner_text().lower()

            print(f"[DEBUG] Found link: {href}")
            if href and href.startswith("http") and "genius.com" in href and ("lyrics" in href or song_name.lower() in text):
                genius_url = href
                break

        if not genius_url:
            raise Exception("Genius link not found in Brave results.")

        print(f"[INFO] Genius URL found: {genius_url}")

        # ✅ Step 2: Scrape lyrics from Genius
        page.goto(genius_url, timeout=15000, wait_until="domcontentloaded")
        page.wait_for_selector('div[data-lyrics-container="true"]', timeout=10000)

        lyrics_blocks = page.query_selector_all('div[data-lyrics-container="true"]')
        lyrics = "\n".join(block.inner_text() for block in lyrics_blocks).strip()

        browser.close()

        if not lyrics:
            raise Exception("Lyrics not found on the Genius page.")

        return lyrics
