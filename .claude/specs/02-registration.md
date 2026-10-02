# Spec: Registration

## Overview
Make the existing `/register` page functional. Today the route only renders `register.html` and the form has nowhere to go. This step adds POST handling that validates the submitted name, email and password, stores the new user in the `users` table with a hashed password, and starts a logged-in session. It is the first step that writes user data and sets up Flask's `session`, which login, logout and profile (Steps 3+) build on.

## Depends on
- Step 1 — Database setup (`users` table, `get_db()`, `init_db()`).

## Routes
- `GET /register` — render the registration form (already exists, unchanged) — public
- `POST /register` — validate form, create the user, log them in, redirect — public

On success: store `user_id` in `session` and redirect to `/profile` (currently a placeholder, which is acceptable). On validation failure: re-render `register.html` with an `error` message and HTTP 400, keeping the submitted name and email filled in.

## Database changes
No database changes. The `users` table in `database/db.py` already has `name`, `email` (UNIQUE), `password_hash` and `created_at`.

## Templates
- **Create:** none
- **Modify:** `templates/register.html`
  - Repopulate the `name` and `email` inputs from submitted values on error (`value="{{ name or '' }}"`, `value="{{ email or '' }}"`)
  - Add `minlength="8"` to the password input to match the placeholder
  - Keep `action="/register"` hardcoded, as in the existing file; keep the existing `{% if error %}` block

## Files to change
- `app.py` — import `request`, `redirect`, `url_for`, `session`; set `app.secret_key`; change `/register` to accept `GET` and `POST`
- `templates/register.html` — as described above

## Files to create
- None

## New dependencies
No new dependencies. Use `werkzeug.security.generate_password_hash`, `sqlite3.IntegrityError` and Flask's built-in `session`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash`); never store or log the plain password
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `get_db()` from `database/db.py`; close the connection in a `try/finally`
- Strip whitespace from name and email, and lowercase the email before saving
- Validation (server-side, in this order): all fields present; email contains `@` and a domain; password at least 8 characters
- Duplicate email: catch `sqlite3.IntegrityError` from the UNIQUE constraint (do not pre-check with a separate SELECT) and show "An account with that email already exists"
- Read `app.secret_key` from the `SECRET_KEY` environment variable, falling back to a clearly named dev-only default; do not commit a real secret
- Do not restructure other routes; leave `/login`, `/logout`, `/profile` untouched
- Follow the existing section-banner comment style in `app.py`

## Definition of done
- [ ] `GET /register` still renders the form
- [ ] Submitting a valid name, email and password creates a row in `users` with a hashed password (`password_hash` is not the plain text)
- [ ] After successful registration the browser is redirected to `/profile` and `session["user_id"]` is set to the new user's id
- [ ] Registering with an email that already exists (including `demo@spendly.com`, and the same email in a different case) shows an error and creates no new row
- [ ] A password shorter than 8 characters shows an error and creates no row
- [ ] An empty name or an invalid email shows an error and creates no row
- [ ] On any error the page returns status 400, shows the error in the `.auth-error` box, and keeps the name and email fields filled in (password is cleared)
- [ ] The app starts without errors and the seeded demo user is unaffected
- [ ] No hardcoded hex colours added; all SQL uses `?` placeholders
