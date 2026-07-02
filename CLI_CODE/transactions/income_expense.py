import sqlite3
from utilities.cli_input_helpers import map_transaction_category


def fetch_all_accounts():
    coms = sqlite3.connect("database/FinCLI.db")
    cursor = coms.cursor()
    cursor.execute("SELECT account_id, bank_account_name FROM accounts")
    fetched_accounts = cursor.fetchall()
    avilable_accounts = {
        fetched_accounts[x][0]: fetched_accounts[x][1]
        for x in range(len(fetched_accounts))
    }
    cursor.close()
    coms.close()
    return avilable_accounts


def fetch_account_balances():
    coms = sqlite3.connect("database/FinCLI.db")
    cursor = coms.cursor()
    cursor.execute("SELECT account_id, running_balance FROM accounts")
    accounts_balance = cursor.fetchall()
    balance_data = {
        accounts_balance[x][0]: accounts_balance[x][1]
        for x in range(len(accounts_balance))
    }
    cursor.close()
    coms.close()
    return balance_data


# ! Income logging function
def log_income_tansaction(amount, date_of_transaction):
    avilable_accounts = fetch_all_accounts()
    account_balances = fetch_account_balances()
    for key, value in avilable_accounts.items():
        print(f"[{key}] {value}")
    txn_account = input("Please select your account:  ")
    while int(txn_account) not in avilable_accounts.keys():
        print("Invalid choice! Try again!")
        txn_account = input("Please select your account:  ")

    txn_category = map_transaction_category(1)
    txn_note = input("Transaction Note (50 chars max): ")
    while len(txn_note) not in range(0, 50):
        print("Invalid input! Try again!")
        txn_note = input("Transaction Note (50 chars max): ")

    # ? calculation of data

    updated_balance = account_balances[int(txn_account)] + amount

    # ? triggering sql queries
    coms = sqlite3.connect("database/FinCLI.db")
    cursor = coms.cursor()
    cursor.execute(
        f"""UPDATE accounts
    SET
        running_balance = {updated_balance},
        modified_at = datetime('now', 'localtime')
    WHERE account_id = {int(txn_account)}
    """
    )
    cursor.execute(
        f"INSERT INTO income_expense (txn_amount, entry_type, txn_date,txn_category, account, note) VALUES ({amount}, 'INCOME', '{date_of_transaction}', '{txn_category}','{avilable_accounts[int(txn_account)]}','{txn_note}')"
    )
    coms.commit()
    cursor.close()
    coms.close()


# ! expense logging function
def log_expense_transaction(transaction_amount, transaction_date):
    avilable_accounts = fetch_all_accounts()
    account_balances = fetch_account_balances()

    for key, value in avilable_accounts.items():
        if account_balances[key] < transaction_amount:
            continue
        print(f"[{key}] {value}")

    txn_account = input("Please select your account:  ")

    while int(txn_account) not in avilable_accounts.keys():
        print("Invalid choice! Try again!")
        txn_account = input("Please select your account:  ")

    txn_category = map_transaction_category(0)
    txn_mode = input("Please provide mode of trasnaction (upi/ cash/ card): ")

    txn_note = input("Transaction Note (50 chars max): ")
    while len(txn_note) not in range(0, 50):
        print("Invalid input! Try again!")
        txn_note = input("Transaction Note (50 chars max): ")

    # ? calculation of data

    updated_balance = account_balances[int(txn_account)] - transaction_amount

    # ? triggering sql queries
    coms = sqlite3.connect("database/FinCLI.db")
    cursor = coms.cursor()
    cursor.execute(
        f"""UPDATE accounts
    SET
        running_balance = {updated_balance},
        modified_at = datetime('now', 'localtime')
    WHERE account_id = {int(txn_account)}
    """
    )

    cursor.execute(
        f"INSERT INTO income_expense (txn_amount, entry_type, txn_date,txn_category, account, note) VALUES ({transaction_amount}, 'EXPENSE', '{transaction_date}', '{txn_category}','{avilable_accounts[int(txn_account)]}','{txn_note}')"
    )
    coms.commit()
    cursor.close()
    coms.close()


# ! self transfer logging
def log_self_transfer_transaction(transaction_amount):
    avilable_accounts = fetch_all_accounts()
    account_balances = fetch_account_balances()

    # ! Source account selection
    eligible_source_accounts = []
    for key, value in avilable_accounts.items():
        if account_balances[key] < transaction_amount:
            continue
        eligible_source_accounts.append(key)
        print(f"[{key}] {value}")

    if len(eligible_source_accounts) == 0:
        print("You don't have sufficient balance to record this transaction")

    else:
        txn_account = input("Please select your account:  ")

        while int(txn_account) not in eligible_source_accounts:
            print("Invalid choice! Try again!")
            txn_account = input("Please select your account:  ")
        # ! destination account selection
        eligible_destination_accounts = []
        for key, value in avilable_accounts.items():
            if key == int(txn_account):
                continue
            eligible_destination_accounts.append(key)
            print(f"[{key}] {value}")
        destination_account = input("select account at which money was transferrerd")
        while int(destination_account) not in eligible_destination_accounts:
            print("Invalid choice! Try again!")
            destination_account = input("Please select your account:  ")

        # ! transaction note
        txn_note = input("Transaction Note (50 chars max): ")
        while len(txn_note) not in range(0, 50):
            print("Invalid input! Try again!")
            txn_note = input("Transaction Note (50 chars max): ")

        # ? update balances
        updated_source_balance = account_balances[int(txn_account)] - transaction_amount
        updated_destination_balance = (
            account_balances[int(destination_account)] + transaction_amount
        )

        # ? posting to database
        coms = sqlite3.connect("database/FinCLI.db")
        cursor = coms.cursor()

        cursor.execute(
            f""" UPDATE accounts 
                    SET 
                        running_balance = {updated_source_balance},
                        modified_at = datetime('now', 'localtime')
                    WHERE account_id = {int(txn_account)}"""
        )

        cursor.execute(
            f""" UPDATE accounts 
                    SET 
                        running_balance = {updated_destination_balance},
                        modified_at = datetime('now', 'localtime')
                    WHERE account_id = {int(destination_account)}"""
        )
        coms.commit()
        cursor.close()
        coms.close()
