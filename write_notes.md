**Implementation Overview (no code)**

1. **Branch and cleanup**
   * `feature/registeration` already exists and is checked out.
   * All remaining uncommitted changes are in the spec files; no other files are staged.
   * No other pending tasks or conflicting merges.

2. **Open and inspect `app.py`**
   * Contains a stub for `@app.route("/register")`.
   * The view should now be updated to handle both `GET` and `POST`.
   * `GET` simply renders `templates/register.html`.
   * `POST` pulls `name`, `email`, `password` from `request.form`.
   * Validation chain:
     1. **Presence**: all fields required.
     2. **Password policy**: at least 8 chars, contains letter and number.
     3. **Email format**: basic regex.
     4. **Uniqueness**: query `users` table for existing email.
   * On failure: re‑render form with `error`, preserving `name` and `email` values.
   * On success: hash password with `generate_password_hash`, insert into `users`, commit, set `session['user_id']`, redirect to the landing page.

3. **Open and inspect `templates/register.html`**
   * Must extend `base.html`.
   * Replace hard‑coded form action `action="/register"` with `action="{{ url_for('register') }}"`.
   * Wrap the fields in `<div class="form-group">` per existing style.
   * Add `{% if error %}<div class="auth-error">{{ error }}</div>{% endif %}` near the top.
   * Add `value="{{ name or '' }}"` and `value="{{ email or '' }}"` to preserve input on error.
   * Ensure that the `required` attribute is present on each input.

4. **Template styling notes**
   * Use CSS variables for colors (e.g., `var(--button-bg)` for the register button).
   * Do not hard‑code hex colors.

5. **Session handling**
   * After inserting a row, obtain `cursor.lastrowid` and store in `session['user_id']`.
   * Ensure `app.secret_key` is set (already present in `app.py`).

6. **Database access**
   * Use parameterised queries: e.g., `db.execute("SELECT id FROM users WHERE email = ?", (email,))`.
   * No use of SQLAlchemy or any ORM.

7. **Error paths**
   * For missing fields: set `error = "X is required."`.
   * For weak password: set `error = "Password must be at least 8 characters, include a letter and a number."`.
   * For invalid email: `error = "Invalid email address."`.
   * For duplicate email: `error = "Email already in use."`.

8. **Unit tests** (to be added later)
   * POST valid data → 302 redirect to `/` and `session['user_id']` set.
   * POST duplicate email → stay on `/register` with error message.
   * POST invalid email or weak password → stay on `/register` with appropriate error.
   * GET `/register` returns 200 and renders form.

9. **Documentation/Comments**
   * Add brief doctrings to the view function.
   * Inline comments for each validation step.

10. **Edge Cases**
   * Trim whitespace from `name` and `email`.
   * Ensure `password` is not stored.
   * Redirect not replaced by `flash` messages; errors are passed in template context.

**Result**: After implementing above, the `/register` feature will meet the spec, adhere to all rules, and be fully tested. No code is provided here per the instruction; the above outlines the implementation plan in detail.
---