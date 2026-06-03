# ? making connection to the fincli database
import sqlite3
from tabulate import tabulate

# todo: STUDY HOW CURSOR WORKS AND HOW .fetchone() works and how does cursor.fetchone() knows what row we are talking about to fetch


def append_transaction(
    txn_date, txn_type, txn_amount, txn_category, txn_account, txn_mode, txn_note
):
    # ? connecting to the database
    coms = sqlite3.connect("database/fincil.db")
    cursor = coms.cursor()

    # ? defining table schemas
    cursor.execute(f"""INSERT INTO transactions
                   (txn_date, txn_type, txn_amount, txn_category, txn_account, txn_mode, txn_note)
                   VALUES 
                   ("{txn_date}","{txn_type}",{txn_amount},"{txn_category}","{txn_account}","{txn_mode}","{txn_note}")
                   """)

    # ? commiting the schema changes into the db
    coms.commit()

    # # the following code fetches last row from the sqlite db named fincli.db for this project and print in console as a summary of recorded trasnaction, last row because the last row is tge latest transaction
    cursor.execute(
        """SELECT txn_date, txn_type, txn_amount, txn_category, txn_account, txn_mode, txn_note FROM transactions
               ORDER BY txn_id DESC
               LIMIT 1;
               """
    )
    txn_latest = list(cursor.fetchone())

    # ? closig cursor and connections
    cursor.close()
    coms.close()

    print(
        tabulate(
            [txn_latest],
            headers=[
                "Date",
                "Type",
                "Amt",
                "Category",
                "Mode",
                "Account",
                "Description",
            ],
            tablefmt="heavy_grid",
        )
    )
