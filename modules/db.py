import sqlite3
import pandas as pd

def get_conn():
    conn = sqlite3.connect("data/dividend_data.db", check_same_thread=False)
    return conn

def get_all_stocks():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM portfolio", conn)
    conn.close()
    return df
