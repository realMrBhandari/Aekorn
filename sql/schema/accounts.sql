CREATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bank_account_name TEXT NOT NULL,
        running_balance REAL NOT NULL,
        account_status TEXT NOT NULL DEFAULT('ACTIVE') CHECK (account_status in ('ACTIVE', 'REMOVED')),
        created_on TEXT DEFAULT(datetime('now')) NOT NULL,
        modified_at TEXT
        ); 