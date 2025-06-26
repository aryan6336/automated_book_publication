# scrape_runner.py

from scrape_chapter import scrape_chapter_from_url
import sys

if __name__ == "__main__":
    url = sys.argv[1]
    scrape_chapter_from_url(url, save_path="output/chapter1.txt")
