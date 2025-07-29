# database/db.py

import sqlite3
from config import DATABASE_PATH

def get_connection():
    return sqlite3.connect(DATABASE_PATH, check_same_thread=False)

def init_db():
    with get_connection() as conn:
        c = conn.cursor()

        # พอร์ตหุ้น
        c.execute('''CREATE TABLE IF NOT EXISTS portfolio (
                        symbol TEXT,
                        group_name TEXT,
                        sector TEXT,
                        avg_price REAL,
                        quantity INTEGER,
                        total_cost REAL
                    )''')

        # ปันผลย้อนหลัง
        c.execute('''CREATE TABLE IF NOT EXISTS dividends (
                        symbol TEXT,
                        xd_date TEXT,
                        payment_date TEXT,
                        dividend REAL,
                        year INTEGER
                    )''')

        # Favorite หุ้น
        c.execute('''CREATE TABLE IF NOT EXISTS favorites (
                        symbol TEXT PRIMARY KEY,
                        note TEXT,
                        added_at TEXT
                    )''')

        # เป้าหมายรายปี
        c.execute('''CREATE TABLE IF NOT EXISTS goals (
                        year INTEGER PRIMARY KEY,
                        goal_amount REAL
                    )''')

        conn.commit()

def add_stock(symbol, group_name, sector, avg_price, quantity):
    total_cost = avg_price * quantity
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO portfolio (symbol, group_name, sector, avg_price, quantity, total_cost)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (symbol.upper(), group_name, sector, avg_price, quantity, total_cost))
        conn.commit()

def delete_stock(symbol):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM portfolio WHERE symbol=?", (symbol.upper(),))
        conn.commit()

def get_portfolio():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM portfolio").fetchall()

def get_favorites():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM favorites").fetchall()

def add_favorite(symbol, note, added_at):
    with get_connection() as conn:
        conn.execute("INSERT OR REPLACE INTO favorites (symbol, note, added_at) VALUES (?, ?, ?)",
                     (symbol.upper(), note, added_at))
        conn.commit()

def delete_favorite(symbol):
    with get_connection() as conn:
        conn.execute("DELETE FROM favorites WHERE symbol=?", (symbol.upper(),))
        conn.commit()

def save_dividend(symbol, xd_date, payment_date, dividend, year):
    with get_connection() as conn:
        conn.execute('''INSERT INTO dividends (symbol, xd_date, payment_date, dividend, year)
                        VALUES (?, ?, ?, ?, ?)''',
                     (symbol.upper(), xd_date, payment_date, dividend, year))
        conn.commit()

def get_dividend_by_month(year):
    with get_connection() as conn:
        rows = conn.execute('''
            SELECT symbol, xd_date FROM dividends WHERE year=?
        ''', (year,)).fetchall()
        return rows
