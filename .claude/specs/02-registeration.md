# Spec: Registeration

## Overview
Provide a public `POST /register` endpoint that creates a new user account, hashes the password, and starts a session. This is the first public‑facing feature needed for user‑onboarding.

## Depends on
None – no prior steps are required.

## Routes
- `GET /register` — public — renders the registration form.
- `POST /register` — public — accepts form data (name, email, password); validates input, creates a new user, and logs them in.

## Database changes
No new tables. Uses existing `users` table (id, name, email, password_hash, created_at).

## Templates
- **Modify**: `templates/register.html` — display validation errors and preserve entered name/email on a failed submission.

## Files to change
- `app.py`
- `templates/register.html`

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs.
- Parameterised queries only.
- Passwords hashed with `werkzeug` (`generate_password_hash`).
- Use CSS variables – no hard‑coded hex values.
- All templates extend `base.html`.

## Definition of done
- Submitting valid name/email/password creates a user, sets `session["user_id"]`, and redirects to the landing page.
- Submitting a duplicate email re-renders the form with "Email already in use."
- Submitting a weak password (under 8 characters, or missing a letter/number) re-renders the form with a validation error.
- Submitting an invalid email format re-renders the form with "Invalid email address."
- Password is stored as a werkzeug hash, never in plain text.