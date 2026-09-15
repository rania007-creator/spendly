import os
import sqlite3
import datetime
from werkzeug.security import generate_password_hash
from flask import g

# Path to the SQLite database file – located in the project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DATABASE = os.path.join(BASE_DIR, "spendly.db")


def _get_db():
    """Return a SQLite connection tied to the current request.
    Caches the connection on ``g`` and ensures foreign‑key support.
    """
    if "sqlite_db" not in g:
        conn = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        g.sqlite_db = conn
    return g.sqlite_db


def get_db():
    """Public helper used by the application and tests."""
    return _get_db()


def init_db():
    """Create the database schema.
    If the old ``app.db`` file exists, delete it to avoid confusion.
    Drops any existing ``categories`` table (removed in the spec).
    """
    # Delete legacy file if it exists
    old_db_path = os.path.join(BASE_DIR, "database", "app.db")
    if os.path.exists(old_db_path):
        os.remove(old_db_path)

    db = _get_db()

    # Ensure no legacy table remains
    db.execute("DROP TABLE IF EXISTS categories;")

    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """
    )
    db.commit()


def seed_db():
    """Populate the database with a demo user and sample expenses.
    No duplicate users are inserted if the table already contains data.
    """
    db = _get_db()
    # Quick check – if any user exists, skip seeding
    row = db.execute("SELECT COUNT(*) FROM users").fetchone()
    if row and row[0] > 0:
        return

    # Insert demo user
    demo_password = generate_password_hash("demo123")
    db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", demo_password),
    )
    user_id = db.execute(
        "SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)
    ).fetchone()[0]

    # Prepare sample expenses – at least one per required category
    categories = [
        "Food",
        "Transport",
        "Bills",
        "Health",
        "Entertainment",
        "Shopping",
        "Other",
    ]
    today = datetime.date.today()
    # Generate dates spread across the current month (days 1-28)
    expenses = [
        {
            "user_id": user_id,
            "amount": 12.50,
            "category": "Food",
            "date": f"{today.year}-{today.month:02d}-01",
            "description": "Lunch",
        },
        {
            "user_id": user_id,
            "amount": 45.30,
            "category": "Transport",
            "date": f"{today.year}-{today.month:02d}-03",
            "description": "Bus fare",
        },
        {
            "user_id": user_id,
            "amount": 89.99,
            "category": "Bills",
            "date": f"{today.year}-{today.month:02d}-07",
            "description": "Electricity",
        },
        {
            "user_id": user_id,
            "amount": 54.20,
            "category": "Health",
            "date": f"{today.year}-{today.month:02d}-10",
            "description": "Medicine",
        },
        {
            "user_id": user_id,
            "amount": 28.00,
            "category": "Entertainment",
            "date": f"{today.year}-{today.month:02d}-15",
            "description": "Movie",
        },
        {
            "user_id": user_id,
            "amount": 19.99,
            "category": "Shopping",
            "date": f"{today.year}-{today.month:02d}-20",
            "description": "Clothes",
        },
        {
            "user_id": user_id,
            "amount": 110.00,
            "category": "Other",
            "date": f"{today.year}-{today.month:02d}-25",
            "description": "Misc",
        },
        {
            "user_id": user_id,
            "amount": 33.33,
            "category": "Food",
            "date": f"{today.year}-{today.month:02d}-28",
            "description": "Dinner",
        },
    ]

    for exp in expenses:
        db.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            (exp["user_id"], exp["amount"], exp["category"], exp["date"], exp["description"]),
        )
    db.commit()
