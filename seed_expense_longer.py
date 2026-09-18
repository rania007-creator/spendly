import sqlite3, random
from datetime import datetime

DB_PATH = "spendly.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

categories = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]

# Add 5 expenses for user_id 2
for i in range(5):
    category = random.choice(categories)
    amount = round(random.uniform(10, 200), 2)
    date = datetime.now().strftime("%Y-%m-%d")
    description = f"Generated expense {i+1}"
    cur.execute(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        (2, amount, category, date, description)
    )

conn.commit()
conn.close()
print("5 new expenses added for user 2.")
