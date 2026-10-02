import os
import sqlite3
from datetime import date

from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "expense_tracker.db"
)


# --- Connection --- #

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# --- Schema --- #

def init_db():
    conn = get_db()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT NOT NULL,
                email         TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at    TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                amount      REAL NOT NULL,
                category    TEXT NOT NULL,
                date        TEXT NOT NULL,
                description TEXT,
                created_at  TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            """
        )
        conn.commit()
    finally:
        conn.close()


# --- Seed data --- #

def seed_db():
    conn = get_db()
    try:
        if conn.execute("SELECT 1 FROM users LIMIT 1").fetchone():
            return

        cur = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
        )
        user_id = cur.lastrowid

        today = date.today()

        def day(n):
            return today.replace(day=n).isoformat()

        # Amounts are in INR (₹)
        expenses = [
            (user_id, 450.0, "Food", "Lunch at Saravana Bhavan", day(1)),
            (user_id, 1200.0, "Transport", "Monthly metro pass", day(3)),
            (user_id, 899.0, "Bills", "Jio recharge", day(5)),
            (user_id, 1800.0, "Health", "Pharmacy and checkup", day(8)),
            (user_id, 350.0, "Entertainment", "Movie tickets", day(12)),
            (user_id, 2599.0, "Shopping", "Running shoes", day(15)),
            (user_id, 500.0, "Other", "Temple donation", day(20)),
            (user_id, 620.0, "Food", "Groceries from BigBasket", day(25)),
        ]
        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, description, date) "
            "VALUES (?, ?, ?, ?, ?)",
            expenses,
        )
        conn.commit()
    finally:
        conn.close()
