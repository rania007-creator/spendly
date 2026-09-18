import sqlite3, random
from datetime import datetime

DB_PATH = "spendly.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

categories = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]

# We'll add 3 expenses for user_id 2
for i in range(3):
    category = random.choice(categories)
    amount = round(random.uniform(5, 100), 2)
    date = datetime.now().strftime("%Y-%m-%d")
    description = f"Test expense {i+1}"
    cur.execute(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        (2, amount, category, date, description)
    )

conn.commit()
conn.close()

print("seeded 3 new expenses for user 2.")
