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
    def fetch_account_balances():
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
