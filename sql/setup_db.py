import sqlite3


def create_database():
    # ? Establishing connection to the database and enabling cursor
    coms = sqlite3.connect("database/fincil.db")
    cursor = coms.cursor()

    # ! defining table schemas
    cursor.execute("""CREATE TABLE transactions(
                  txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  txn_date TEXT NOT NULL CHECK (txn_date >= '2001-09-16'),
                  txn_type TEXT NOT NULL CHECK (txn_type IN ("CREDIT", "DEBIT")),
                  txn_amount REAL NOT NULL CHECK(txn_amount > 0),
                  txn_category TEXT NOT NULL,
                  txn_account TEXT NOT NULL CHECK(length(txn_account) <= 100),
                  txn_mode TEXT NOT NULL CHECK(length(txn_mode) <= 25),
                  txn_note TEXT,
                  recorded_on TEXT DEFAULT(datetime('now')) NOT NULL)""")

    # ? commiting the schema changes into the db
    coms.commit()

    # ? closig cursor and connections
    cursor.close()
    coms.close()

    print("database created sucessfully")
