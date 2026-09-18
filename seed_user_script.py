import sqlite3
import random
from datetime import datetime
from werkzeug.security import generate_password_hash

DB_PATH = "spendly.db"

first_names = ["Rahul", "Priya", "Amit", "Sneha", "Vikram",
               "Ananya", "Rohan", "Kavya", "Arjun", "Divya"]
last_names = ["Sharma", "Patel", "Reddy", "Iyer", "Singh",
              "Gupta", "Nair", "Rao", "Mehta", "Kapoor"]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

while True:
    first = random.choice(first_names)
    last = random.choice(last_names)
    name = f"{first} {last}"
    suffix = random.randint(10, 999)
    email = f"{first.lower()}.{last.lower()}{suffix}@gmail.com"

    cur.execute("SELECT 1 FROM users WHERE email = ?", (email,))
    if cur.fetchone() is None:
        break

password_hash = generate_password_hash("password123")
created_at = datetime.now().isoformat()

cur.execute(
    "INSERT INTO users (name, email, password_hash, created_at) "
    "VALUES (?, ?, ?, ?)",
    (name, email, password_hash, created_at)
)
conn.commit()

new_id = cur.lastrowid
print(f"id: {new_id}")
print(f"name: {name}")
print(f"email: {email}")

conn.close()
