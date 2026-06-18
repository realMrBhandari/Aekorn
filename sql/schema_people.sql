-- ! schema for people table for borrow & lend & return transactions
CREATE TABLE IF NOT EXISTS people (
    person_id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_name TEXT NOT NULL,
    relationship TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT(datetime('now'))
);