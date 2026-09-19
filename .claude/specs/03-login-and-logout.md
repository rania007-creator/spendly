# Spec: Login and Logout

## Overview
This feature implements a complete user authentication flow for the Spendly expense tracker. A POST `/login` endpoint validates credentials against the `users` table, creates a session for the authenticated user, and redirects them to the landing page. The complementary `/logout` endpoint clears the session, ensuring that protected routes can enforce access control.

This step is required before exposing any CRUD expense routes because those routes depend on authenticated users to associate expenses with a firm. It also demonstrates the project’s pattern of using Werkzeug’s password hashing utilities and Flask’s session support.

## Depends on
- Registeration feature (creating the `users` table and populating users) – see spec `02-registeration.md`.
- Database initialization (`app.app_context()`, `init_db`, `seed_db`).

## Routes
- `GET /login` — public, renders the login form.
- `POST /login` — public, accepts `email` and `password`, authenticates the user, and stores the user id in the Flask session (`session['user_id']`). On success redirects to `/`. On failure re‑renders the form with an error message.
- `GET /logout` — logged-in only, clears the session and redirects to `/`.

## Database changes
No new tables. Uses the existing `users` table (id, name, email, password_hash, created_at).

## Templates
- **Modify**: `templates/login.html` – update the form to POST to `/login` and display any authentication error passed from the view.

## Files to change
- `app.py`
- `templates/login.html`

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- Use plain SQL with parameterised queries (no ORM).  Statements like `SELECT id FROM users WHERE email = ?` are acceptable.
- Validate credentials with `werkzeug.security.check_password_hash`.
- Store the user id in `session['user_id']` and clear it on logout.
- Do **not** store plain‑text passwords.
- Use CSS variables defined in `static/css/style.css`; do not hard‑code hex colors.
- All templates continue to extend `base.html`.

## Definition of done
- Submitting a valid email/password with a user in the `users` table authenticates the user and redirects to the landing page.
- Submitting an invalid email or password re-renders the login form with a user‑friendly error message.
- Visiting `/logout` after logging in clears the session cookie and redirects to `/`.
- No hard‑coded hex colors appear in new CSS.
- No ORM code is introduced.
