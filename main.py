from scraper.scrape import scrape_books
from storage.db import init_db, save_books
from report.generate import generate_report

def run_pipeline():
    print("--- Starting scraping pipeline ---")

    print("\n[1/3] Initialising database...")
    init_db()

    print("\n[2/3] Scraping books...")
    df = scrape_books()

    print("\n[3/3] Saving to database...")
    save_books(df)

    print("\nGenerating report preview...")
    html = generate_report()
    with open("report/preview_report.html", "w") as f:
        f.write(html)

    print("\n--- Pipeline complete ---")
    print("Open report/preview_report.html in your browser to preview")

if __name__ == "__main__":
    run_pipeline()