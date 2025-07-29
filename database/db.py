import sqlite3

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
