from database.connection import get_connection

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    tariff TEXT DEFAULT 'Free',
    checks_left INTEGER DEFAULT 1,
    subscription_end TEXT,
    token TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS contracts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    contract_type TEXT,
    role TEXT,
    source_text TEXT,
    char_count INTEGER,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    contract_id INTEGER,
    model TEXT,
    report TEXT,
    rating INTEGER,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    tariff TEXT,
    period TEXT,
    amount REAL,
    status TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
"""


def init_db():
    conn = get_connection()
    conn.executescript(SCHEMA)
    try:
        conn.execute("ALTER TABLE users ADD COLUMN token TEXT")
    except Exception:
        pass
    conn.commit()
    conn.close()