# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

"Spendly" is a Flask-based expense tracker built as a step-by-step learning project. Many pieces are intentionally left as stubs/placeholders for the student to implement — check a file's contents before assuming a feature is missing or broken; it may just be an unimplemented step.

## Commands

Windows, PowerShell, venv at `venv/` (Python 3.13):

```powershell
# Activate the virtual environment
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the dev server (http://localhost:5001, debug mode on)
python app.py

# Run tests (pytest + pytest-flask are declared, but no test files exist yet)
pytest
```

## Architecture

- `app.py` — single Flask app instance and all routes. There is no blueprint split; new routes get added directly here.
- `database/db.py` — intended to hold `get_db()` (SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (create tables with `CREATE TABLE IF NOT EXISTS`), and `seed_db()` (sample data). As of now this is just a comment describing what to build (Step 1) — no schema exists yet. `database/__init__.py` is empty.
- `templates/` — Jinja2 templates. `base.html` defines the shared layout (nav, footer, font/CSS includes) with `{% block title %}`, `{% block head %}`, `{% block content %}`, `{% block scripts %}`; page templates extend it.
- `static/css/style.css` — single global stylesheet for all pages (design tokens/vars-based, no per-page CSS files).
- `static/js/main.js` — currently empty; global client-side JS goes here.
- SQLite database file is `expense_tracker.db` at the project root once created (git-ignored, not present until `init_db()`/`seed_db()` is implemented and run).

## Route status

| Route | Status |
|---|---|
| `/`, `/register`, `/login`, `/terms`, `/privacy` | Implemented — render a template, no backend logic yet (forms don't POST-handle) |
| `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete` | Placeholder — return a bare string, explicitly marked `# students will implement these` in `app.py`, tied to later steps (Step 3/4/7/8/9) |

Don't assume a placeholder route is broken — it's an intentional stub. When implementing one, replace the placeholder body entirely rather than layering logic around the `"... — coming in Step N"` string.

## Tech constraints

- Stdlib `sqlite3` only — no ORM (SQLAlchemy etc. is not in `requirements.txt`). `database/db.py` should use raw SQL via `sqlite3`.
- No auth/session library beyond what Flask/Werkzeug ship with (e.g. `werkzeug.security` for password hashing, Flask's built-in `session`). Don't add Flask-Login or similar without asking.
- No frontend framework or build step — plain Jinja2 templates, one global `style.css`, one global `main.js`, no bundler/npm.
- Keep new dependencies out of `requirements.txt` unless the step actually needs them; this is a teaching project, so the dependency surface is intentionally minimal.

## Code style

- Python: 4-space indent, section-banner comments (`# --- Label --- #`, see `app.py`) to separate logical groups of routes/functions.
- CSS: 4-space indent, kebab-case class names, all colors/fonts/spacing as `var(--token)` custom properties defined in `:root` (see top of `style.css`) rather than hardcoded values; same `/* --- Label --- */` banner comments to separate sections.
- Templates: extend `base.html` via `{% extends %}` and fill in `{% block content %}` (and `title`/`head`/`scripts` as needed) rather than duplicating the `<html>`/nav/footer scaffold.
- Follow existing patterns exactly when finishing a stubbed file — `database/db.py`'s header comment already specifies the exact function names/signatures (`get_db()`, `init_db()`, `seed_db()`) expected of it.

## Warnings / things to avoid

- Don't rewrite or restructure the implemented routes/templates while implementing placeholders — this is a step-by-step course repo, so changes should be scoped to the step being worked on.
- Don't introduce an ORM, a CSS framework, or a JS framework — everything here is deliberately hand-rolled for learning purposes.
- Form actions are hardcoded strings (e.g. `action="/register"`) rather than `{{ url_for(...) }}` in some templates — match the existing pattern in a given file rather than "fixing" it to `url_for` unless asked.
- `expense_tracker.db` and `venv/` are git-ignored — never commit them, and don't hand-edit the `.db` file directly; go through `db.py`.
- The stray `Screenshot 2026-03-25 at 12.36.20 AM.png` and `.DS_Store` at the project root aren't part of the app — don't reference them from code, and flag before deleting since they may be the user's own files.

## Notes

- The app runs on port 5001, not Flask's default 5000.
- `.claude/plans/` is git-ignored.
