# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Common Commands

### 1. Install dependencies
```bash
python -m pip install -r requirements.txt
```

The repository already contains a virtual environment in `venv/`.  Activate it before installing:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Run the development server
The application is a plain Flask app.  The `app.py` script starts the server with debugging enabled on port **5001**.

```bash
# Option 1 – direct execution (debug mode baked in)
python app.py

# Option 2 – Flask CLI (explicit environment variables)
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --port 5001
```

The Flask CLI gives you the usual `flask` commands, while the direct execution route keeps the process very small for quick tests.

### 3. Run tests
Unit and integration tests are written with **pytest** (and the `pytest-flask` plugin for Flask fixtures).

```bash
pytest
```

If you only want to run a single test file or function, pass the path or pattern:
```bash
pytest tests/test_login.py
pytest tests/test_login.py::test_valid_login
```

### 4. Linting / Formatting
While there is no linting configuration shipped with the repository, the typical tooling that works with the current dependencies is Python’s `black` and `flake8`.  All commands are run against the root of the repository.

```bash
black .          # format code in place
flake8 .         # discover style violations
```

Feel free to add a `pyproject.toml` or `.flake8` file if you want to enforce stricter rules.

---

## High‑Level Code Architecture

```
└── expense‑tracker/                 # project root
    ├── app.py                       # Flask entry point
    ├── database/
    │   ├── __init__.py
    │   └── db.py                     # SQLite helper (placeholder)
    ├── static/
    │   ├── css/style.css            # UI styling for the landing page and auth screens
    │   └── js/main.js               # Hook for future interactive features
    ├── templates/
    │   ├── base.html                # Layout and common header/footer
    │   ├── landing.html             # Home page
    │   ├── register.html            # Sign‑up form
    │   ├── login.html               # Sign‑in form
    │   ├── terms.html               # Terms & Conditions page
    │   └── privacy.html             # Privacy Policy page
    └── requirements.txt             # Runtime dependencies
```

### Core Pieces

* **`app.py`** – Instantiates the Flask app, defines the URL routes, and provides stub endpoints for the future expense‑tracking features.

* **`templates/`** – Implements Jinja2 templates.  The *base* template includes the navigation bar and footer; child templates supply page‑specific content.

* **`static/`** – Holds global CSS and very lightweight JavaScript that drives the hero‑section modal.  As new UI components are added, they will live under `templates/` and be styled here.

* **`database/db.py`** – Placeholder for SQLite helper functions (`get_db()`, `init_db()`, `seed_db()`).  When the scaffold evolves into a persistence‑backed application, database logic, migrations, and ORM models will be added here.

### What’s next

The project is a *lesson plan* style starter: the current “Student” comment markers in `db.py` and the route stubs in `app.py` indicate where the learning modules will gradually expand.

The following directions summarize the next actionable changes for a developer:

1. **Implement `db.py`** – build a simple SQLite connection pool, create the tables for users, expenses, and categories.
2. **Add CRUD routes** – enable `/expenses/add`, `/expenses/<int:id>/edit`, and `/expenses/<int:id>/delete` with HTML forms.
3. **Add authentication** – implement a session‑based login / logout system that protects the CRUD endpoints.
4. **Wire tests** – create a `tests/` package that covers the API endpoints using `pytest-flask` fixtures.

These steps are covered in subsequent GitHub Issues or the in‑repo learning guides.

---

## Miscellaneous

* **Virtual environment** – The `venv/` folder is present; activate it before running anything.
* **Static file reference** – The Jinja `url_for('static', filename='js/main.js')` lookup works for the JavaScript modal.
* **Flask debugging** – The supplied `app.run(debug=True, port=5001)` is good for local experimentation.  For production, flip the debug flag and switch to a WSGI server.

Feel free to copy‑paste the commands above into your terminal to bootstrap, run, and test this project. Happy coding!
