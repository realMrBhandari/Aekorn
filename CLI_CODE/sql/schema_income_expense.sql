CREATE TABLE IF NOT EXISTS income_expense (
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    txn_amount REAL NOT NULL CHECK(txn_amount > 0),
    entry_type TEXT NOT NULL CHECK(entry_type IN ('INCOME', 'EXPENSE')),
    txn_date TEXT NOT NULL CHECK(txn_date > '2001-09-16'),
    txn_category TEXT NOT NULL,
    account TEXT NOT NULL,
    note TEXT,
    created_on TEXT NOT NULL DEFAULT(datetime('now','localtime'))
);

-- ? todo add trasnaction mode as well 