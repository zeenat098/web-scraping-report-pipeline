import pandas as pd
from storage.db import load_latest, load_all

def generate_report():
    df      = load_latest()
    df_all  = load_all()

    total_books     = len(df)
    avg_price       = round(df["price"].mean(), 2)
    avg_rating      = round(df["rating"].mean(), 2)
    in_stock        = len(df[df["availability"] == "In stock"])
    scraped_date    = df["scraped_date"].max()

    top_rated = (
        df[df["rating"] == 5]
        .sort_values("price")
        .head(5)[["title", "price", "rating"]]
    )

    cheapest = (
        df.sort_values("price")
        .head(5)[["title", "price", "rating"]]
    )

    by_rating = (
        df.groupby("rating")
        .agg(count=("title", "count"), avg_price=("price", "mean"))
        .round(2)
        .reset_index()
    )

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px;
                    margin: 0 auto; padding: 20px; color: #333; }}
            h1   {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            h2   {{ color: #2980b9; margin-top: 30px; }}
            .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }}
            .kpi {{ background: #f8f9fa; border-left: 4px solid #3498db;
                    padding: 15px; border-radius: 4px; }}
            .kpi .value {{ font-size: 28px; font-weight: bold; color: #2c3e50; }}
            .kpi .label {{ font-size: 12px; color: #7f8c8d; margin-top: 5px; }}
            table  {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th     {{ background: #3498db; color: white; padding: 10px; text-align: left; }}
            td     {{ padding: 8px 10px; border-bottom: 1px solid #eee; }}
            tr:nth-child(even) {{ background: #f8f9fa; }}
        </style>
    </head>
    <body>
        <h1>Weekly Books Report</h1>
        <p>Scraped on: <strong>{scraped_date}</strong></p>

        <div class="kpi-grid">
            <div class="kpi"><div class="value">{total_books}</div>
                <div class="label">Total Books</div></div>
            <div class="kpi"><div class="value">${avg_price}</div>
                <div class="label">Avg Price</div></div>
            <div class="kpi"><div class="value">{avg_rating}</div>
                <div class="label">Avg Rating</div></div>
            <div class="kpi"><div class="value">{in_stock}</div>
                <div class="label">In Stock</div></div>
        </div>

        <h2>Top rated books under lowest price</h2>
        {top_rated.to_html(index=False)}

        <h2>Cheapest books</h2>
        {cheapest.to_html(index=False)}

        <h2>Books by rating</h2>
        {by_rating.to_html(index=False)}
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    html = generate_report()
    with open("report/preview_report.html", "w") as f:
        f.write(html)
    print("Report saved to report/preview_report.html")