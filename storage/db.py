import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/books.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            title         TEXT,
            price         REAL,
            rating        INTEGER,
            availability  TEXT,
            url           TEXT,
            scraped_date  TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialised")

def save_books(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("books", conn, if_exists="append", index=False)
    conn.close()
    print(f"Saved {len(df)} rows to database")

def load_latest():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("""
        SELECT * FROM books
        WHERE scraped_date = (SELECT MAX(scraped_date) FROM books)
    """, conn)
    conn.close()
    return df

def load_all():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM books ORDER BY scraped_date", conn)
    conn.close()
    return df

if __name__ == "__main__":
    init_db()
    print("DB ready at", DB_PATH)