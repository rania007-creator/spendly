from flask import Flask, render_template, g
from database.db import get_db, init_db, seed_db
app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/register")
def register():
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

# Ensure the database is initialized and seeded before the app starts.
# This runs automatically when the Flask application is executed
# directly (e.g., python app.py). It is wrapped in an app context to
# provide the required Flask request state.
with app.app_context():
    init_db()
    seed_db()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
