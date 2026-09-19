from flask import Flask, render_template, g, request, redirect, url_for, session
import re
import os
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db

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
        elif len(password) < 8 or not re.search(r"(?=.*[A-Za-z])(?=.*\\d)", password):
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
        return redirect(url_for("landing"))

    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

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
