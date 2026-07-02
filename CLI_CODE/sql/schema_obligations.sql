-- ! schema for table obligations responsible for borrow & lend transactions 
CREATE TABLE IF NOT EXISTS obligations (
    obligation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    person TEXT NOT NULL,
    obligation_type TEXT NOT NULL CHECK(obligation_type IN ('LEND', 'BORROW')),
    obligation_date TEXT NOT NULL CHECK(obligation_date >= '2001-09-16'),
    due_date TEXT CHECK(due_date IS NULL OR due_date > obligation_date),
    principal_amt REAL NOT NULL CHECK(principal_amt > 0),
    returned_amt REAL NOT NULL DEFAULT 0 CHECK(returned_amt >= 0 AND returned_amt <= principal_amt),
    due_amt REAL GENERATED ALWAYS AS (principal_amt - returned_amt) VIRTUAL,
    obligation_status TEXT NOT NULL DEFAULT 'ACTIVE'
        CHECK(obligation_status IN ('ACTIVE', 'CLOSED')),
    closure_date TEXT
        CHECK(closure_date IS NULL OR closure_date > obligation_date),
    created_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
);