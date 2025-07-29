import sqlite3
import sqlite3

DB_FILE = "dividends.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def get_portfolio():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT symbol, "group", sector, avg_price, quantity
        FROM portfolio
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows
def init_db():
    conn = sqlite3.connect("dividends.db")
    cursor = conn.cursor()

    # ตัวอย่าง table สามารถปรับตาม schema จริง
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            shares INTEGER,
            average_cost REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dividends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            amount REAL,
            xd_date TEXT
        )
    """)

    conn.commit()
    conn.close()
