from flask import Flask, render_template, g, request, redirect, url_for, session
from functools import wraps
import re
import os
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db


def is_authenticated():
    """Return True if a user id exists in the session."""
    return session.get("user_id") is not None


def login_required(view):
    """Decorator that redirects to /login if the user is not logged‑in."""
    @wraps(view)
    def wrapped_view(**kwargs):
        if not is_authenticated():
            return redirect(url_for("login"))
        return view(**kwargs)
    return wrapped_view

# Helper for avatar initials

def _avatar_initials(name: str) -> str:
    """Return the first letters of the first two words of the name.
    If only one word, use its first two characters.
    """
    parts = name.strip().split()
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[1][0]).upper()

# ------------------------------------------------------------------ #
# Flask app setup                                                   #
# ------------------------------------------------------------------ #
app = Flask(__name__)
# In production this should come from an environment variable.
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

@app.route("/")
def landing():
    return render_template("landing.html")

# ------------------------------------------------------------------ #
# Registration & authentication
# ------------------------------------------------------------------ #
@app.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration. Supports GET to show form and POST to process data."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        error = None

        # Basic field presence
        if not name:
            error = "Name is required."
        elif not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."
        # Password policy
        elif len(password) < 8 or not re.search(r"(?=.*[A-Za-z])(?=.*\d)", password):
            error = "Password must be at least 8 characters, include a letter and a number."
        # Email format
        elif not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            error = "Invalid email address."
        else:
            db = get_db()
            existing = db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
            if existing:
                error = "Email already in use."

        if error:
            return render_template("register.html", error=error, name=name, email=email)

        # Create user and log them in
        password_hash = generate_password_hash(password)
        db = get_db()
        cursor = db.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        db.commit()
        user_id = cursor.lastrowid
        session["user_id"] = user_id
        # Store name and email for navbar display
        session["name"] = name
        session["email"] = email
        return redirect(url_for("landing"))

    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

# POST handler for login
@app.route("/login", methods=["POST"])
def login_post():
    """Handle user login. Validates credentials, logs in, redirects."""
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    error = None

    if not email or not password:
        error = "Email and password are required."
    else:
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        if user is None or not check_password_hash(user["password_hash"], password):
            error = "Invalid credentials."

    if error:
        return render_template("login.html", error=error, email=email)

    session["user_id"] = user["id"]
    # Store name and email for navbar display
    session["name"] = user["name"]
    session["email"] = user["email"]
    return redirect(url_for("landing"))

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("landing"))

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

# ------------------------------------------------------------------ #
# Profile route
# ------------------------------------------------------------------ #
@app.route("/profile")
@login_required
def profile():
    context = {
        "user": {
            "name": session.get("name", "User"),
            "email": session.get("email", "user@example.com"),
            "avatar_initials": _avatar_initials(session.get("name", "User")),
            "member_since": "2023-01-01",
        },
        "summary": {
            "total_spent": 1234.56,
            "transaction_count": 42,
            "top_category": "Food",
        },
        "transactions": [
            {"date": "2025-09-19", "description": "Groceries", "category": "Food", "amount": 12.34},
            {"date": "2025-09-18", "description": "Taxi", "category": "Transport", "amount": 23.45},
            {"date": "2025-09-17", "description": "Lunch", "category": "Food", "amount": 9.99},
        ],
        "categories": [
            {"name": "Food", "total": 256.78},
            {"name": "Transport", "total": 120.50},
            {"name": "Bills", "total": 420.00},
        ],
    }
    return render_template("profile.html", **context)

# ------------------------------------------------------------------ #
# Database lifecycle helpers                                          #
# ------------------------------------------------------------------ #
@app.teardown_appcontext
def close_db(error=None):
    """Close the SQLite connection after each request."""
    db = getattr(g, "sqlite_db", None)
    if db is not None:
        db.close()

# ------------------------------------------------------------------ #
# Flask‑CLI commands – used by developers to bootstrap the DB      #
# ------------------------------------------------------------------ #
@app.cli.command("init-db")
def init_db_command():
    """Initialize the database schema in a fresh SQLite file."""
    init_db()
    print("Initialized the database schema.")

@app.cli.command("seed-db")
def seed_db_command():
    """Populate the database with a demo user and sample expenses."""
    seed_db()
    print("Seeded the database with sample data.")

# ------------------------------------------------------------------ #
# Bootstrap the database on application startup (app.app_context())   #
# ------------------------------------------------------------------ #
with app.app_context():
    init_db()
    seed_db()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
