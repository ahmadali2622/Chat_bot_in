"""
scraper.py
----------
Simple web scraper for the NETSOL Technologies website.

What it does (step by step):
1. Visit a list of NETSOL pages.
2. Download the HTML of each page using `requests`.
3. Use BeautifulSoup to pull out the clean, readable text (no HTML tags).
4. Save everything into one text file: scraped_data.txt

Run it with:
    python scraper.py

This file is saved and later used by build_index.py to create the
RAG knowledge base.
"""

import requests
from bs4 import BeautifulSoup
import time

# ---------------------------
# 1. Pages we want to scrape
# ---------------------------
# Add or remove URLs here depending on which pages you want the chatbot
# to know about.
PAGES_TO_SCRAPE = [
    "https://netsoltech.com/en-us",
    "https://netsoltech.com/en-us/about-us",
    "https://netsoltech.com/en-us/products",
    "https://netsoltech.com/en-us/services",
    "https://netsoltech.com/en-us/industries",
    "https://netsoltech.com/en-us/contact-us",
]

OUTPUT_FILE = "scraped_data.txt"

# Some websites block requests that don't look like they're coming from
# a real browser. Adding a User-Agent header fixes most "403 Forbidden" errors.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


def scrape_page(url: str) -> str:
    """
    Downloads one page and returns its clean text content.
    Returns an empty string if the page could not be fetched.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print(f"  Skipped (status {response.status_code}): {url}")
            return ""

        soup = BeautifulSoup(response.content, "html.parser")

        # Remove tags that don't contain useful text (scripts, styles, nav menus)
        for tag in soup(["script", "style", "nav", "footer", "noscript"]):
            tag.decompose()

        # get_text() pulls out everything that is actual readable text
        text = soup.get_text(separator="\n")

        # Clean up extra blank lines/spaces
        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line]  # drop empty lines
        clean_text = "\n".join(lines)

        return clean_text

    except requests.RequestException as e:
        print(f"  Error fetching {url}: {e}")
        return ""


def main():
    all_text = []

    print("Starting scrape...")
    for url in PAGES_TO_SCRAPE:
        print(f"Scraping: {url}")
        page_text = scrape_page(url)

        if page_text:
            # Mark where each page starts/ends so build_index.py
            # can split things back up if needed later.
            all_text.append(f"\n\n----- PAGE: {url} -----\n\n")
            all_text.append(page_text)

        time.sleep(1)  # small delay so we don't hammer the server

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("".join(all_text))

    print(f"\nDone! Saved scraped text to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
