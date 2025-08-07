# config.py

# Theme configuration
THEME = {
    "primary_color": "#FF6B00",     # ปุ่มสีส้ม
    "background_color": "#1E1E1E",  # สีพื้นหลังเข้ม
    "text_color": "#FFFFFF",
    "secondary_text": "#AAAAAA",
    "accent_color": "#FF6B00",
    "pie_colors": [
        "#FFD700",  # COMM
        "#4169E1",  # TOURISM
        "#32CD32",  # BANK
        "#8A2BE2",  # HELTH
        "#228B22",  # ENERG
        "#FF69B4",  # Others
    ],
}

# Portfolio settings
PORTFOLIO_COLS = [
    "symbol",
    "group",
    "sector",
    "avg_price",
    "quantity",
    "total_cost",
    "latest_price",
    "market_value",
    "gain_loss",
    "dividend_yield",
    "dividend_total",
]

# Database
DATABASE_PATH = "database/database.db"

# Target goal
DEFAULT_ANNUAL_GOAL = 50000  # บาทต่อปี

# Month labels (Thai)
MONTH_LABELS = [
    "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.",
    "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.",
    "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."
]
