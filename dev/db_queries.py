#  THIS FILE IS ONLY RESPONSIBLE FOR TALKING WITH DATABASE, INSERT, UPDATE, DELETE. Most of the data transfer between python and sqlite will happen through this. Since state was not required hence defining class with static methods.
import sqlite3


class QueryHandler:

    @staticmethod
    def fetch_account_mapping():
        connection = sqlite3.connect("database/FinCLI.db")
        cursor = connection.cursor()
        cursor.execute("SELECT account_id, bank_account_name FROM accounts")
        accounts_fetched = cursor.fetchall()
        mapped_accounts = {
            accounts_fetched[x][0]: accounts_fetched[x][1]
            for x in range(len(accounts_fetched))
        }
        cursor.close()
        connection.close()
        return mapped_accounts

    @staticmethod
    def fetch_all_account_balances():
        connection = sqlite3.connect("database/FinCLI.db")
        cursor = connection.cursor()
        cursor.execute("SELECT account_id, running_balance FROM accounts")
        accounts_balance = cursor.fetchall()
        balance_data = {
            accounts_balance[x][0]: accounts_balance[x][1]
            for x in range(len(accounts_balance))
        }
        cursor.close()
        connection.close()
        return balance_data

    @staticmethod
    def get_individual_balance(account_id):
        connection = sqlite3.connect("database/FinCLI.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT running_balance FROM accounts WHERE account_id = ?", (account_id,)
        )
        fetched_balance = cursor.fetchall()
        running_balance = fetched_balance[0][0]
        cursor.close()
        connection.close()
        return running_balance

    @staticmethod
    def update_account_balance(cur, account_id, new_balance):
        with open("sql/update_account.sql", "r") as file:
            cur.execute(file.read(), (account_id, new_balance))

    @staticmethod
    def log_income_transaction(
        amt, date, category, account_id, note, cur, type="INCOME"
    ):
        with open("sql/insert_income_expense.sql", "r") as file:
            cur.execute(file.read(), (amt, type, date, category, account_id, note))

    @staticmethod
    def log_expense_transaction(
        amt, date, category, account_id, note, cur, type="EXPENSE"
    ):
        with open("sql/insert_income_expense.sql", "r") as file:
            cur.execute(file.read(), (amt, type, date, category, account_id, note))
