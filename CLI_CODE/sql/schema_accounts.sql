-- ! Schema for user bank accounts

CREATE TABLE IF NOT EXISTS accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
      bank_account_name TEXT NOT NULL,
    running_balance REAL NOT NULL CHECK (running_balance >= 0),
    account_status TEXT NOT NULL DEFAULT 'ACTIVE'
        CHECK (account_status IN ('ACTIVE', 'INACTIVE')),
    created_on TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    modified_at TEXT
);