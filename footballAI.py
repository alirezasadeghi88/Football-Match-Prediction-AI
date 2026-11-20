

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


def add_team(name):

    try:
        # اضافه کردن نام تیم به جدول
        cursor.execute(
            "INSERT INTO teams (name) VALUES (?)",
            (name,)
        )

        # ذخیره اطلاعات
        conn.commit()

        print("تیم با موفقیت اضافه شد!")

    except sqlite3.IntegrityError:
        # جلوگیری از ثبت نام تکراری
        print("این تیم قبلاً ثبت شده است!")
        
        
def add_match(home, away, hg, ag):

    # بررسی وجود تیم‌ها در دیتابیس
    cursor.execute(
        "SELECT name FROM teams WHERE name IN (?, ?)",
        (home, away)
    )

    found = {row[0] for row in cursor.fetchall()}

    if home not in found or away not in found:
        print("یک یا هر دو تیم در دیتابیس وجود ندارند!")
        return

    # بررسی معتبر بودن اطلاعات
    if home == away or hg < 0 or ag < 0:
        print("اطلاعات مسابقه نامعتبر است!")
        return

    # ذخیره مسابقه در دیتابیس
    cursor.execute("""
        INSERT INTO matches
        (home_team, away_team, home_goals, away_goals)
        VALUES (?, ?, ?, ?)
    """, (home, away, hg, ag))

    conn.commit()

    print("مسابقه با موفقیت ذخیره شد!")
    
    
def get_stats(team):

    # دریافت مسابقات تیم از دیتابیس
    cursor.execute("""
        SELECT home_team, away_team, home_goals, away_goals
        FROM matches
        WHERE home_team = ? OR away_team = ?
    """, (team, team))

    games = cursor.fetchall()

    # بررسی وجود مسابقه
    if not games:
        return None

    # مقداردهی اولیه آمار
    gf = ga = points = wins = draws = losses = 0

    # بررسی مسابقات
    for home, away, hg, ag in games:

        # تشخیص میزبان یا مهمان بودن تیم
        if home == team:
            scored, conceded = hg, ag
        else:
            scored, conceded = ag, hg

        # محاسبه گل زده و خورده
        gf += scored
        ga += conceded

        # محاسبه نتیجه مسابقه
        if scored > conceded:
            wins += 1
            points += 3

        elif scored == conceded:
            draws += 1
            points += 1

        else:
            losses += 1

    # تعداد کل مسابقات
    total = len(games)

    # برگرداندن آمار تیم
    return {
        "games": total,
        "gf": gf / total,
        "ga": ga / total,
        "points": points,
        "wins": wins,
        "draws": draws,
        "losses": losses
    }
    
    

def show_stats(team):

    # دریافت آمار تیم
    stats = get_stats(team)

    if stats is None:
        print("اطلاعات مسابقه‌ای برای این تیم وجود ندارد!")
        return

    print("\nنام تیم:", team)
    print("تعداد بازی:", stats["games"])
    print("میانگین گل زده:", round(stats["gf"], 2))
    print("میانگین گل خورده:", round(stats["ga"], 2))
    print("امتیازات:", stats["points"])
    print("تعداد برد:", stats["wins"])
    print("تعداد مساوی:", stats["draws"])
    print("تعداد باخت:", stats["losses"])