import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"

RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3,
    "Four": 4, "Five": 5
}

def scrape_books():
    books = []
    url = START_URL

    print("Scraping books.toscrape.com...")

    while url:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for article in soup.select("article.product_pod"):
            title  = article.h3.a["title"]
            price_text = article.select_one(".price_color").text
            price  = float(price_text.encode("ascii", "ignore").decode().strip()[1:])
            rating = RATING_MAP.get(article.p["class"][1], 0)
            avail  = article.select_one(".availability").text.strip()
            link   = BASE_URL + article.h3.a["href"].replace("../", "")

            books.append({
                "title":       title,
                "price":       price,
                "rating":      rating,
                "availability": avail,
                "url":         link,
                "scraped_date": date.today().isoformat()
            })

        next_btn = soup.select_one("li.next a")
        url = BASE_URL + next_btn["href"] if next_btn else None

    df = pd.DataFrame(books)
    print(f"Scraped {len(df)} books")
    return df

if __name__ == "__main__":
    df = scrape_books()
    print(df.head())