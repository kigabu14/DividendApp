import sqlite3

DB_FILE = "database.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # สร้างตารางพอร์ตหุ้น
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            "group" TEXT,
            sector TEXT,
            avg_price REAL,
            quantity INTEGER
        );
    """)

    # สร้างตารางรายการ favorite
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL UNIQUE
        );
    """)

    conn.commit()
    conn.close()

# ดึงข้อมูลพอร์ตหุ้นทั้งหมด
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

# ---------------- FAVORITE FUNCTIONS ----------------

# สร้างตาราง favorites
def create_favorites_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()

# ดึงรายการ favorite ทั้งหมด
def get_favorites():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT symbol FROM favorites")
    rows = [row[0] for row in cursor.fetchall()]
    conn.close()
    return rows

# เพิ่ม favorite
def add_favorite(symbol):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO favorites (symbol) VALUES (?)", (symbol,))
    conn.commit()
    conn.close()

# ลบ favorite
def remove_favorite(symbol):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favorites WHERE symbol = ?", (symbol,))
    conn.commit()
    conn.close()
