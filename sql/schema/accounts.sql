REATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bank_account_name TEXT NOT NULL,
        running_balance REAL NOT NULL,
        created_on TEXT DEFAULT(datetime('now')) NOT NULL)