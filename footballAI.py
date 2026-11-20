

import sqlite3

# اتصال به دیتابیس فوتبال
# اگر فایل دیتابیس وجود نداشته باشد، ساخته می‌شود
conn = sqlite3.connect("football.db")

# ایجاد ابزار اجرای دستورات SQL
cursor = conn.cursor()

# ساخت جدول تیم‌ها
cursor.execute("""
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")

# ساخت جدول مسابقات
cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    home_team TEXT,
    away_team TEXT,
    home_goals INTEGER,
    away_goals INTEGER
)
""")

# ذخیره تغییرات در دیتابیس
conn.commit()