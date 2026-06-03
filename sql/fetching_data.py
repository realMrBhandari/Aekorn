import sqlite3


def fetch_All_tranasctions():
    # ! This function serves but one master: transaction_history
    coms = sqlite3.connect("database/fincil.db")
    cursor = coms.cursor()

    # ? fetch all transactions recorded so far in descending order otbo transaction date
    cursor.execute(
        """SELECT txn_date, txn_type, txn_amount, txn_category, txn_account, txn_mode, txn_note FROM transactions
               ORDER BY txn_date DESC"""
    )

    # ? getting all the fetched transaction using fetchall() function and saving it into transactions
    transactions = cursor.fetchall()

    cursor.close()
    coms.close()
    # ? returning the values stored in transactions, based on my obervation it is sotred as list with tuples as values
    return transactions


def fetch__Recent_tranasctions():
    coms = sqlite3.connect("database/fincil.db")
    cursor = coms.cursor()
    cursor.execute(
        """SELECT txn_type, txn_amount, txn_mode, txn_category, txn_date FROM transactions
        ORDER BY txn_date DESC"""
    )
    transactions = cursor.fetchmany(5)
    cursor.close()
    coms.close()
    # ? returning the values stored in transactions, based on my obervation it is sotred as list with tuples as values
    return transactions
