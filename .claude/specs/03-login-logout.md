# Spec: Login and Logout

## Overview
Make the existing `/login` page functional and replace the `/logout` placeholder. Today `/login` only renders `login.html` and the form has nowhere to go, and `/logout` returns a bare string. This step adds POST handling that checks the submitted email and password against the `users` table (using werkzeug's hash check), starts a session on success, and adds a logout that clears the session. Together with Step 2 (registration) this completes the basic authentication cycle that profile and expense routes (Steps 4+) rely on.

## Depends on
- Step 1 — Database setup (`users` table, `get_db()`, seeded demo user).
- Step 2 — Registration (`app.secret_key` and `session["user_id"]` convention).

## Routes
- `GET /login` — render the login form (already exists) — public. If already logged in, redirect to `/` (landing page).
- `POST /login` — validate credentials, set `session["user_id"]`, redirect to `/` (landing page) — public
- `GET /logout` — clear the session and redirect to `/` (landing) — logged-in (harmless if not logged in)

On invalid credentials: re-render `login.html` with a generic `error` ("Invalid email or password") and HTTP 400, keeping the submitted email filled in. Do not reveal whether the email exists.

## Database changes
No database changes. The `users` table already has `email` (UNIQUE) and `password_hash`.

## Templates
- **Create:** none
- **Modify:**
  - `templates/login.html` — repopulate the email input on error (`value="{{ email or '' }}"`); keep `action="/login"` hardcoded and the existing `{% if error %}` block
  - `templates/base.html` — make the navbar session-aware: when `session.get("user_id")` is set show a "Sign out" link to `url_for('logout')` (and a "Profile" link) instead of "Sign in" / "Get started"; otherwise keep the current links

## Files to change
- `app.py` — import `check_password_hash`; change `/login` to accept `GET` and `POST`; replace the `/logout` placeholder body (move it out of the placeholder section into the implemented routes, following the banner style)
- `templates/login.html` — as described above
- `templates/base.html` — as described above

## Files to create
- None

## New dependencies
No new dependencies. Use `werkzeug.security.check_password_hash` and Flask's built-in `session`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug — verify with `check_password_hash`; never compare or log plain passwords
- Use CSS variables — never hardcode hex values (only add CSS if the navbar change needs it, in `style.css` using existing tokens)
- All templates extend `base.html`
- Use `get_db()` from `database/db.py`; close the connection in a `try/finally`
- Strip whitespace and lowercase the email before lookup (matches how registration stores it)
- Same error message and status for unknown email and wrong password
- Empty email or password shows "All fields are required" with HTTP 400
- Logout uses `session.clear()` and redirects with `url_for("landing")`
- Do not restructure `/register` or other routes; leave `/profile` and expense placeholders untouched
- Follow the existing section-banner comment style in `app.py`

## Definition of done
- [ ] `GET /login` renders the form when logged out
- [ ] Logging in as `demo@spendly.com` / `demo123` redirects to `/` and sets `session["user_id"]`
- [ ] The email is matched case-insensitively and ignoring surrounding whitespace
- [ ] A wrong password and an unknown email both show "Invalid email or password" in the `.auth-error` box with status 400, and the email field stays filled in
- [ ] Empty fields show an error with status 400
- [ ] A user created through `/register` can log out and log back in with the same credentials
- [ ] `GET /logout` clears the session and redirects to `/`; visiting `/login` afterwards shows the form again
- [ ] Visiting `/login` while logged in redirects to `/`
- [ ] The navbar shows "Sign out" when logged in and "Sign in" / "Get started" when logged out
- [ ] The app starts without errors; no hardcoded hex colours added; all SQL uses `?` placeholders
