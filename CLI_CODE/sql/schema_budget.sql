CREATE TABLE IF NOT EXISTS budgets (
    budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
    budget_month TEXT NOT NULL UNIQUE,
    budget_amount REAL NOT NULL CHECK(budget_amount > 0),
    created_at TEXT NOT NULL DEFAULT(datetime('now','localtime')),
    modified_at TEXT
);